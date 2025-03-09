import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count, Q
from django.db import transaction

from store_app.models import Store, StoreReview, StoreSocialMedia
from store_app.serializers import StoreSerializer, StoreReviewSerializer, StoreSocialMediaSerializer

def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt
def store_list(request):
    if request.method == 'GET':
        # Filter parameters
        seller_id = request.GET.get('seller')
        status = request.GET.get('status')
        search = request.GET.get('search')
        
        stores = Store.objects.all()
        
        if seller_id:
            stores = stores.filter(seller_id=seller_id)
        
        if status:
            stores = stores.filter(status=status)
        
        if search:
            stores = stores.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        result = [StoreSerializer.serialize(store) for store in stores]
        return JsonResponse(result, safe=False)
    
    elif request.method == 'POST':
        data = parse_request_body(request)
        required_fields = ['seller_id', 'name']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            store = Store.objects.create(
                seller_id=data['seller_id'],
                name=data['name'],
                description=data.get('description', ''),
                logo_url=data.get('logo_url'),
                banner_url=data.get('banner_url'),
                status=data.get('status', 'active')
            )
            
            # Process social media links if provided
            if 'social_media' in data and isinstance(data['social_media'], list):
                for social in data['social_media']:
                    if 'media_type' in social and 'url' in social:
                        StoreSocialMedia.objects.create(
                            store=store,
                            media_type=social['media_type'],
                            url=social['url'],
                            display_name=social.get('display_name')
                        )
            
            return JsonResponse(StoreSerializer.serialize(store, include_social_media=True), status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def store_detail(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
        
        if request.method == 'GET':
            include_reviews = request.GET.get('reviews', 'false').lower() == 'true'
            include_social_media = request.GET.get('social_media', 'false').lower() == 'true'
            
            return JsonResponse(StoreSerializer.serialize(
                store, 
                include_reviews=include_reviews,
                include_social_media=include_social_media
            ))
        
        elif request.method == 'PUT':
            data = parse_request_body(request)
            
            # Update store fields
            if 'name' in data:
                store.name = data['name']
            if 'description' in data:
                store.description = data['description']
            if 'logo_url' in data:
                store.logo_url = data['logo_url']
            if 'banner_url' in data:
                store.banner_url = data['banner_url']
            if 'status' in data:
                store.status = data['status']
                
            store.save()
            return JsonResponse(StoreSerializer.serialize(store))
        
        elif request.method == 'DELETE':
            store.delete()
            return JsonResponse({'message': 'Store deleted successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def store_reviews(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
        
        if request.method == 'GET':
            reviews = StoreReview.objects.filter(store=store).order_by('-created_at')
            result = [StoreReviewSerializer.serialize(review) for review in reviews]
            return JsonResponse(result, safe=False)
        
        elif request.method == 'POST':
            data = parse_request_body(request)
            required_fields = ['user_id', 'rating']
            
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if not (1 <= data['rating'] <= 5):
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
            
            # Check if user has already reviewed this store
            existing_review = StoreReview.objects.filter(store=store, user_id=data['user_id']).first()
            
            with transaction.atomic():
                if existing_review:
                    # Update existing review
                    existing_review.rating = data['rating']
                    existing_review.comment = data.get('comment', '')
                    existing_review.save()
                    review = existing_review
                else:
                    # Create new review
                    review = StoreReview.objects.create(
                        store=store,
                        user_id=data['user_id'],
                        rating=data['rating'],
                        comment=data.get('comment', '')
                    )
                    # Increment review count
                    store.review_count += 1
                
                # Update store average rating
                avg_rating = StoreReview.objects.filter(store=store).aggregate(Avg('rating'))['rating__avg'] or 0
                store.rating = round(avg_rating, 2)
                store.save()
                
                return JsonResponse(StoreReviewSerializer.serialize(review), status=201 if not existing_review else 200)
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def store_social_media(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
        
        if request.method == 'GET':
            social_media = StoreSocialMedia.objects.filter(store=store)
            result = [StoreSocialMediaSerializer.serialize(social) for social in social_media]
            return JsonResponse(result, safe=False)
        
        elif request.method == 'POST':
            data = parse_request_body(request)
            required_fields = ['media_type', 'url']
            
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if data['media_type'] not in dict(StoreSocialMedia.SOCIAL_MEDIA_TYPES):
                return JsonResponse({'error': 'Invalid media type'}, status=400)
            
            social_media = StoreSocialMedia.objects.create(
                store=store,
                media_type=data['media_type'],
                url=data['url'],
                display_name=data.get('display_name')
            )
            
            return JsonResponse(StoreSocialMediaSerializer.serialize(social_media), status=201)
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
