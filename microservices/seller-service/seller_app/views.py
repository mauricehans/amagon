import json
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Avg
from django.db import transaction

from seller_app.models import Seller, SellerAnalytics
from seller_app.serializers import SellerSerializer, SellerAnalyticsSerializer

def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt
def seller_list(request):
    if request.method == 'GET':
        # Filter parameters
        status = request.GET.get('status')
        
        sellers = Seller.objects.all()
        
        if status:
            sellers = sellers.filter(status=status)
        
        result = [SellerSerializer.serialize(seller) for seller in sellers]
        return JsonResponse(result, safe=False)
    
    elif request.method == 'POST':
        data = parse_request_body(request)
        required_fields = ['user_id', 'company_name', 'contact_email', 'address']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if seller already exists for this user
        if Seller.objects.filter(user_id=data['user_id']).exists():
            return JsonResponse({'error': 'Seller already exists for this user'}, status=400)
        
        try:
            seller = Seller.objects.create(
                user_id=data['user_id'],
                company_name=data['company_name'],
                description=data.get('description', ''),
                contact_email=data['contact_email'],
                contact_phone=data.get('contact_phone', ''),
                address=data['address'],
                logo_url=data.get('logo_url'),
                tax_id=data.get('tax_id'),
                business_license=data.get('business_license'),
                status=data.get('status', 'pending'),
                commission_rate=data.get('commission_rate', 5.00)
            )
            
            return JsonResponse(SellerSerializer.serialize(seller), status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def seller_detail(request, seller_id=None, user_id=None):
    try:
        if seller_id:
            seller = Seller.objects.get(id=seller_id)
        elif user_id:
            seller = Seller.objects.get(user_id=user_id)
        else:
            return JsonResponse({'error': 'Seller ID or User ID is required'}, status=400)
        
        if request.method == 'GET':
            return JsonResponse(SellerSerializer.serialize(seller))
        
        elif request.method == 'PUT':
            data = parse_request_body(request)
            
            # Update seller fields
            if 'company_name' in data:
                seller.company_name = data['company_name']
            if 'description' in data:
                seller.description = data['description']
            if 'contact_email' in data:
                seller.contact_email = data['contact_email']
            if 'contact_phone' in data:
                seller.contact_phone = data['contact_phone']
            if 'address' in data:
                seller.address = data['address']
            if 'logo_url' in data:
                seller.logo_url = data['logo_url']
            if 'tax_id' in data:
                seller.tax_id = data['tax_id']
            if 'business_license' in data:
                seller.business_license = data['business_license']
            if 'status' in data:
                seller.status = data['status']
            if 'commission_rate' in data:
                seller.commission_rate = data['commission_rate']
                
            seller.save()
            return JsonResponse(SellerSerializer.serialize(seller))
        
        elif request.method == 'DELETE':
            seller.delete()
            return JsonResponse({'message': 'Seller deleted successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Seller.DoesNotExist:
        return JsonResponse({'error': 'Seller not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def seller_analytics(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
        
        if request.method == 'GET':
            # Date range parameters
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            
            analytics = SellerAnalytics.objects.filter(seller=seller)
            
            if start_date:
                analytics = analytics.filter(date__gte=start_date)
            
            if end_date:
                analytics = analytics.filter(date__lte=end_date)
            
            # Order by date
            analytics = analytics.order_by('date')
            
            result = [SellerAnalyticsSerializer.serialize(analytic) for analytic in analytics]
            return JsonResponse(result, safe=False)
        
        elif request.method == 'POST':
            data = parse_request_body(request)
            required_fields = ['date', 'total_sales', 'total_orders']
            
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Format the date
            try:
                date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
            
            # Check if analytics already exist for this date
            existing = SellerAnalytics.objects.filter(seller=seller, date=date).first()
            
            if existing:
                # Update existing analytics
                existing.total_sales = data['total_sales']
                existing.total_orders = data['total_orders']
                existing.average_order_value = data.get('average_order_value', 0)
                existing.products_sold = data.get('products_sold', 0)
                existing.commission_paid = data.get('commission_paid', 0)
                existing.views = data.get('views', 0)
                existing.conversion_rate = data.get('conversion_rate', 0)
                existing.save()
                
                return JsonResponse(SellerAnalyticsSerializer.serialize(existing))
            else:
                # Create new analytics
                analytics = SellerAnalytics.objects.create(
                    seller=seller,
                    date=date,
                    total_sales=data['total_sales'],
                    total_orders=data['total_orders'],
                    average_order_value=data.get('average_order_value', 0),
                    products_sold=data.get('products_sold', 0),
                    commission_paid=data.get('commission_paid', 0),
                    views=data.get('views', 0),
                    conversion_rate=data.get('conversion_rate', 0)
                )
                
                return JsonResponse(SellerAnalyticsSerializer.serialize(analytics), status=201)
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Seller.DoesNotExist:
        return JsonResponse({'error': 'Seller not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
