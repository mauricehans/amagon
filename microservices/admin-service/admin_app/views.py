import os
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse
from .models import AdminSettings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_app.settings')

application = get_wsgi_application()


def admin_settings_list(request):
    settings = AdminSettings.objects.all()
    return JsonResponse({'settings': list(settings.values())})


def admin_settings_detail(request, setting_id):
    # Implémentation à compléter
    pass


def system_logs(request):
    # Implémentation à compléter
    pass


def system_log_detail(request, log_id):
    # Implémentation à compléter
    pass
