import json
from product_app.models import Product, Category, Review

class CategorySerializer:
    @staticmethod
    def serialize(category, include_children=False):
        result = {
            'id': str(category.id),
            'name': category.name,
            'description': category.description,
            'parent_id': str(category.parent.id) if category.parent else None,
            'created_at': category.created_at.isoformat(),
            'updated_at': category.updated_at.isoformat(),
        }
        
        if include_children:
            result['children'] = [
                CategorySerializer.serialize(child, False) 
                for child in category.children.all()
            ]
            
        return result
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class ProductSerializer:
    @staticmethod
    def serialize(product, include_reviews=False):
        result = {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'category': CategorySerializer.serialize(product.category),
            'seller_id': str(product.seller_id),
            'image_url': product.image_url,
            'is_active': product.is_active,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat(),
        }
        
        if include_reviews:
            result['reviews'] = [
                ReviewSerializer.serialize(review) 
                for review in Review.objects.filter(product=product)
            ]
            
        return result
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class ReviewSerializer:
    @staticmethod
    def serialize(review):
        return {
            'id': str(review.id),
            'product_id': str(review.product.id),
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
