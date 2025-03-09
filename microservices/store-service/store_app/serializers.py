import json
from store_app.models import Store, StoreReview, StoreSocialMedia

class StoreSocialMediaSerializer:
    @staticmethod
    def serialize(social_media):
        return {
            'id': str(social_media.id),
            'store_id': str(social_media.store.id),
            'media_type': social_media.media_type,
            'url': social_media.url,
            'display_name': social_media.display_name,
            'created_at': social_media.created_at.isoformat(),
            'updated_at': social_media.updated_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class StoreReviewSerializer:
    @staticmethod
    def serialize(review):
        return {
            'id': str(review.id),
            'store_id': str(review.store.id),
            'user_id': str(review.user_id),
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class StoreSerializer:
    @staticmethod
    def serialize(store, include_reviews=False, include_social_media=False):
        result = {
            'id': str(store.id),
            'seller_id': str(store.seller_id),
            'name': store.name,
            'description': store.description,
            'logo_url': store.logo_url,
            'banner_url': store.banner_url,
            'status': store.status,
            'rating': float(store.rating),
            'review_count': store.review_count,
            'created_at': store.created_at.isoformat(),
            'updated_at': store.updated_at.isoformat(),
        }
        
        if include_reviews:
            reviews = StoreReview.objects.filter(store=store).order_by('-created_at')
            result['reviews'] = [StoreReviewSerializer.serialize(review) for review in reviews]
        
        if include_social_media:
            social_media = StoreSocialMedia.objects.filter(store=store)
            result['social_media'] = [StoreSocialMediaSerializer.serialize(social) for social in social_media]
            
        return result
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data
