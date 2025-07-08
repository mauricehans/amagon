from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import hashlib
import os
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    salt = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def set_password(self, raw_password):
        if not self.salt:
            self.salt = os.urandom(8).hex()
        self.password = hashlib.md5((self.salt + raw_password).encode()).hexdigest()

    def check_password(self, raw_password):
        return self.password == hashlib.md5((self.salt + raw_password).encode()).hexdigest()

class UserToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_tokens'

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = os.urandom(32).hex()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expires_at < timezone.now()