import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone

from admin_app.models import AdminSettings, SystemLog
from admin_app.serializers import AdminSettingsSerializer, SystemLogSerializer

def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt
def admin_settings_list(request):
    if request.method == 'GET':
        # Get public parameter
        is_public = request.GET.get('public')
        
        if is_public and is_public.lower() == 'true':
            settings = AdminSettings.objects.filter(is_public=True)
        else:
            settings = AdminSettings.objects.all()
        
        result = [AdminSettingsSerializer.serialize(setting) for setting in settings]
        return JsonResponse(result, safe=False)
    
    elif request.method == 'POST':
        data = parse_request_body(request)
        required_fields = ['name', 'value']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if setting already exists
        if AdminSettings.objects.filter(name=data['name']).exists():
            return JsonResponse({'error': 'Setting with this name already exists'}, status=400)
        
        try:
            setting = AdminSettings.objects.create(
                name=data['name'],
                value=data['value'],
                description=data.get('description', ''),
                is_public=data.get('is_public', False),
                updated_by=data.get('updated_by')
            )
            
            return JsonResponse(AdminSettingsSerializer.serialize(setting), status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def admin_settings_detail(request, setting_id=None, setting_name=None):
    try:
        if setting_id:
            setting = AdminSettings.objects.get(id=setting_id)
        elif setting_name:
            setting = AdminSettings.objects.get(name=setting_name)
        else:
            return JsonResponse({'error': 'Setting ID or name is required'}, status=400)
        
        if request.method == 'GET':
            return JsonResponse(AdminSettingsSerializer.serialize(setting))
        
        elif request.method == 'PUT':
            data = parse_request_body(request)
            
            if 'value' in data:
                setting.value = data['value']
            if 'description' in data:
                setting.description = data['description']
            if 'is_public' in data:
                setting.is_public = data['is_public']
            
            setting.updated_by = data.get('updated_by')
            setting.updated_at = timezone.now()
            setting.save()
            
            return JsonResponse(AdminSettingsSerializer.serialize(setting))
        
        elif request.method == 'DELETE':
            setting.delete()
            return JsonResponse({'message': 'Setting deleted successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except AdminSettings.DoesNotExist:
        return JsonResponse({'error': 'Setting not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def system_logs(request):
    if request.method == 'GET':
        # Filtering parameters
        service = request.GET.get('service')
        level = request.GET.get('level')
        user_id = request.GET.get('user_id')
        search = request.GET.get('search')
        
        # Pagination parameters
        limit = int(request.GET.get('limit', 100))
        offset = int(request.GET.get('offset', 0))
        
        logs = SystemLog.objects.all()
        
        if service:
            logs = logs.filter(service=service)
        
        if level:
            logs = logs.filter(level=level)
        
        if user_id:
            logs = logs.filter(user_id=user_id)
        
        if search:
            logs = logs.filter(Q(message__icontains=search) | Q(service__icontains=search))
        
        total_count = logs.count()
        logs = logs[offset:offset+limit]
        
        result = {
            'logs': [SystemLogSerializer.serialize(log) for log in logs],
            'total': total_count,
            'limit': limit,
            'offset': offset
        }
        
        return JsonResponse(result)
    
    elif request.method == 'POST':
        data = parse_request_body(request)
        required_fields = ['service', 'message']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            log = SystemLog.objects.create(
                service=data['service'],
                level=data.get('level', 'info'),
                message=data['message'],
                details=data.get('details'),
                user_id=data.get('user_id'),
                ip_address=data.get('ip_address')
            )
            
            return JsonResponse(SystemLogSerializer.serialize(log), status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def system_log_detail(request, log_id):
    try:
        log = SystemLog.objects.get(id=log_id)
        
        if request.method == 'GET':
            return JsonResponse(SystemLogSerializer.serialize(log))
        
        elif request.method == 'DELETE':
            log.delete()
            return JsonResponse({'message': 'Log deleted successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except SystemLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
