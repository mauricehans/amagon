import json
from admin_app.models import AdminSettings, SystemLog

class AdminSettingsSerializer:
    @staticmethod
    def serialize(settings):
        return {
            'id': str(settings.id),
            'name': settings.name,
            'value': settings.value,
            'description': settings.description,
            'is_public': settings.is_public,
            'created_at': settings.created_at.isoformat(),
            'updated_at': settings.updated_at.isoformat(),
            'updated_by': str(settings.updated_by) if settings.updated_by else None,
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class SystemLogSerializer:
    @staticmethod
    def serialize(log):
        return {
            'id': str(log.id),
            'service': log.service,
            'level': log.level,
            'message': log.message,
            'details': log.details,
            'user_id': str(log.user_id) if log.user_id else None,
            'ip_address': log.ip_address,
            'created_at': log.created_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data
