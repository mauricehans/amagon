from .models import AdminToken
from .security_utils import generate_token
from django.utils import timezone
from datetime import timedelta

def create_admin_token(admin):
    """Crée et sauvegarde un nouveau token pour un administrateur."""
    token = AdminToken.objects.create(
        user=admin,
        token=generate_token(),
        expires_at=timezone.now() + timedelta(days=1)
    )
    return token

def validate_admin_token(token_string):
    """Valide un token et retourne l'administrateur associé."""
    try:
        token = AdminToken.objects.get(token=token_string)
        if token.is_expired():
            token.delete()
            return None
        token.last_used = timezone.now()
        token.save()
        return token.user
    except AdminToken.DoesNotExist:
        return None

def revoke_admin_token(token_string):
    """Révoque un token."""
    try:
        token = AdminToken.objects.get(token=token_string)
        token.delete()
        return True
    except AdminToken.DoesNotExist:
        return False

def cleanup_expired_tokens():
    """Supprime tous les tokens expirés."""
    AdminToken.objects.filter(expires_at__lt=timezone.now()).delete()
