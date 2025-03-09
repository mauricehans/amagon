from django.db import models
import uuid

class AdminSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)  # Whether this setting is visible to non-admin users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.UUIDField(null=True, blank=True)  # User ID of admin who updated

    def __str__(self):
        return self.name

class SystemLog(models.Model):
    LOG_LEVELS = (
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(max_length=100)  # Which service generated this log
    level = models.CharField(max_length=20, choices=LOG_LEVELS, default='info')
    message = models.TextField()
    details = models.JSONField(null=True, blank=True)  # Additional details as JSON
    user_id = models.UUIDField(null=True, blank=True)  # User ID related to log (if applicable)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.level.upper()}] {self.service}: {self.message[:50]}"
    
    class Meta:
        ordering = ['-created_at']
