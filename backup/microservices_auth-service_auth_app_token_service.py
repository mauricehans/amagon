from .models import UserToken
from .security_utils import generate_token
from django.utils import timezone
from datetime import timedelta

def create_user_token(user):
    """Crée et sauvegarde un nouveau token pour un utilisateur."""
    token = UserToken.objects.create(
        user=user,
        token=generate_token(),
        expires_at=timezone.now() + timedelta(days=7)
    )
    return token

def validate_user_token(token_string):
    """Valide un token et retourne l'utilisateur associé."""
    try:
        token = UserToken.objects.get(token=token_string)
        if token.is_expired():
            token.delete()
            return None
        token.last_used = timezone.now()
        token.save()
        return token.user
    except UserToken.DoesNotExist:
        return None

def revoke_user_token(token_string):
    """Révoque un token."""
    try:
        token = UserToken.objects.get(token=token_string)
        token.delete()
        return True
    except UserToken.DoesNotExist:
        return False

def cleanup_expired_tokens():
    """Supprime tous les tokens expirés."""
    UserToken.objects.filter(expires_at__lt=timezone.now()).delete()
