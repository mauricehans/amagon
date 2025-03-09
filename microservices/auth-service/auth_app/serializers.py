import json
from auth_app.models import User, Role, Permission, RolePermission

class UserSerializer:
    @staticmethod
    def serialize(user_instance):
        roles = [{'id': str(role.id), 'name': role.name} 
                for role in user_instance.roles.all()]
        
        return {
            'id': str(user_instance.id),
            'username': user_instance.username,
            'email': user_instance.email,
            'first_name': user_instance.first_name,
            'last_name': user_instance.last_name,
            'roles': roles,
            'is_active': user_instance.is_active,
            'created_at': user_instance.created_at.isoformat() if user_instance.created_at else None,
            'updated_at': user_instance.updated_at.isoformat() if user_instance.updated_at else None,
            'last_login': user_instance.last_login.isoformat() if user_instance.last_login else None,
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class RoleSerializer:
    @staticmethod
    def serialize(role_instance):
        permissions = [{'id': str(rp.permission.id), 'name': rp.permission.name} 
                      for rp in RolePermission.objects.filter(role=role_instance)]
        
        return {
            'id': str(role_instance.id),
            'name': role_instance.name,
            'description': role_instance.description,
            'permissions': permissions,
            'created_at': role_instance.created_at.isoformat(),
            'updated_at': role_instance.updated_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class PermissionSerializer:
    @staticmethod
    def serialize(permission_instance):
        return {
            'id': str(permission_instance.id),
            'name': permission_instance.name,
            'description': permission_instance.description,
            'created_at': permission_instance.created_at.isoformat(),
            'updated_at': permission_instance.updated_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data
