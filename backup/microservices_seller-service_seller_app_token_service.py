from .models import SellerToken
from .security_utils import generate_token
from django.utils import timezone
from datetime import timedelta

def create_seller_token(seller):
    """Crée et sauvegarde un nouveau token pour un vendeur."""
    token = SellerToken.objects.create(
        seller=seller,
        token=generate_token(),
        expires_at=timezone.now() + timedelta(days=7)
    )
    return token

def validate_seller_token(token_string):
    """Valide un token et retourne le vendeur associé."""
    try:
        token = SellerToken.objects.get(token=token_string)
        if token.is_expired():
            token.delete()
            return None
        token.last_used = timezone.now()
        token.save()
        return token.seller
    except SellerToken.DoesNotExist:
        return None

def revoke_seller_token(token_string):
    """Révoque un token."""
    try:
        token = SellerToken.objects.get(token=token_string)
        token.delete()
        return True
    except SellerToken.DoesNotExist:
        return False

def cleanup_expired_tokens():
    """Supprime tous les tokens expirés."""
    SellerToken.objects.filter(expires_at__lt=timezone.now()).delete()
