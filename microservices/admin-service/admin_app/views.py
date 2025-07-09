from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json
import requests

from .models import AdminUser, SupportTicket, TicketMessage, TicketActivity, AdminDashboardStats
from . import token_service

@csrf_exempt
@api_view(['POST'])
def admin_login(request):
    """Connexion admin"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        try:
            admin = AdminUser.objects.get(username=username)
        except AdminUser.DoesNotExist:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

        if not admin.check_password(password):
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token_service.create_admin_token(admin)
        
        return Response({
            'message': 'Connexion réussie',
            'token': token.token,
            'admin': {
                'id': str(admin.id),
                'username': admin.username,
                'email': admin.email,
                'role': admin.role,
                'department': admin.department,
                'is_super_admin': admin.is_super_admin
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def admin_logout(request):
    """Déconnexion admin"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'No authorization token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_string = auth_header.split(' ')[1]
        token_service.revoke_admin_token(token_string)
        
        return Response({'message': 'Déconnexion réussie'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def admin_profile(request):
    """Profil admin"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'admin': {
                'id': str(admin.id),
                'username': admin.username,
                'email': admin.email,
                'role': admin.role,
                'department': admin.department,
                'is_super_admin': admin.is_super_admin
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def admin_dashboard(request):
    """Dashboard principal admin"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Statistiques des tickets
        total_tickets = SupportTicket.objects.count()
        open_tickets = SupportTicket.objects.filter(status='open').count()
        in_progress_tickets = SupportTicket.objects.filter(status='in_progress').count()
        resolved_today = SupportTicket.objects.filter(
            resolved_at__date=timezone.now().date()
        ).count()
        
        # Tickets assignés à cet admin
        my_tickets = SupportTicket.objects.filter(assigned_to=admin).count()
        my_open_tickets = SupportTicket.objects.filter(
            assigned_to=admin, 
            status__in=['open', 'in_progress']
        ).count()
        
        # Tickets récents
        recent_tickets = SupportTicket.objects.select_related('assigned_to').order_by('-created_at')[:10]
        
        # Tickets par priorité
        priority_stats = SupportTicket.objects.values('priority').annotate(
            count=Count('id')
        ).order_by('priority')
        
        # Tickets par catégorie
        category_stats = SupportTicket.objects.values('category').annotate(
            count=Count('id')
        ).order_by('category')
        
        return Response({
            'stats': {
                'total_tickets': total_tickets,
                'open_tickets': open_tickets,
                'in_progress_tickets': in_progress_tickets,
                'resolved_today': resolved_today,
                'my_tickets': my_tickets,
                'my_open_tickets': my_open_tickets,
            },
            'recent_tickets': [{
                'id': str(ticket.id),
                'ticket_number': ticket.ticket_number,
                'subject': ticket.subject,
                'requester_name': ticket.requester_name,
                'requester_type': ticket.requester_type,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'assigned_to': ticket.assigned_to.username if ticket.assigned_to else None,
                'created_at': ticket.created_at.isoformat()
            } for ticket in recent_tickets],
            'priority_stats': list(priority_stats),
            'category_stats': list(category_stats)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard_stats(request):
    """Statistiques détaillées pour le dashboard"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Statistiques des 30 derniers jours
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Évolution des tickets
        daily_tickets = []
        for i in range(30):
            date = (timezone.now() - timedelta(days=i)).date()
            tickets_count = SupportTicket.objects.filter(created_at__date=date).count()
            resolved_count = SupportTicket.objects.filter(resolved_at__date=date).count()
            
            daily_tickets.append({
                'date': date.isoformat(),
                'created': tickets_count,
                'resolved': resolved_count
            })
        
        # Temps de résolution moyen
        avg_resolution_time = SupportTicket.objects.filter(
            resolved_at__isnull=False,
            created_at__gte=thirty_days_ago
        ).aggregate(
            avg_time=Avg('resolved_at') - Avg('created_at')
        )
        
        return Response({
            'daily_tickets': daily_tickets[::-1],  # Inverser pour avoir l'ordre chronologique
            'avg_resolution_time': avg_resolution_time.get('avg_time', 0)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ticket_list(request):
    """Liste des tickets de support avec filtres"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Paramètres de filtrage
        status_filter = request.GET.get('status')
        priority_filter = request.GET.get('priority')
        category_filter = request.GET.get('category')
        assigned_filter = request.GET.get('assigned')
        requester_type_filter = request.GET.get('requester_type')
        search = request.GET.get('search')
        
        # Construire la requête
        tickets = SupportTicket.objects.select_related('assigned_to')
        
        if status_filter:
            tickets = tickets.filter(status=status_filter)
        if priority_filter:
            tickets = tickets.filter(priority=priority_filter)
        if category_filter:
            tickets = tickets.filter(category=category_filter)
        if assigned_filter == 'me':
            tickets = tickets.filter(assigned_to=admin)
        elif assigned_filter == 'unassigned':
            tickets = tickets.filter(assigned_to__isnull=True)
        if requester_type_filter:
            tickets = tickets.filter(requester_type=requester_type_filter)
        if search:
            tickets = tickets.filter(
                Q(ticket_number__icontains=search) |
                Q(subject__icontains=search) |
                Q(requester_name__icontains=search) |
                Q(requester_email__icontains=search)
            )
        
        tickets = tickets.order_by('-created_at')
        
        # Pagination
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        start = (page - 1) * per_page
        end = start + per_page
        
        total_count = tickets.count()
        tickets_page = tickets[start:end]
        
        return Response({
            'tickets': [{
                'id': str(ticket.id),
                'ticket_number': ticket.ticket_number,
                'subject': ticket.subject,
                'description': ticket.description[:200] + '...' if len(ticket.description) > 200 else ticket.description,
                'requester_name': ticket.requester_name,
                'requester_email': ticket.requester_email,
                'requester_type': ticket.requester_type,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'assigned_to': {
                    'id': str(ticket.assigned_to.id),
                    'username': ticket.assigned_to.username
                } if ticket.assigned_to else None,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat()
            } for ticket in tickets_page],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': (total_count + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def ticket_detail(request, ticket_id):
    """Détails d'un ticket de support"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        
        if request.method == 'GET':
            # Récupérer les messages du ticket
            messages = TicketMessage.objects.filter(ticket=ticket).order_by('created_at')
            
            # Récupérer l'historique d'activité
            activities = TicketActivity.objects.filter(ticket=ticket).order_by('-created_at')
            
            return Response({
                'ticket': {
                    'id': str(ticket.id),
                    'ticket_number': ticket.ticket_number,
                    'subject': ticket.subject,
                    'description': ticket.description,
                    'requester_name': ticket.requester_name,
                    'requester_email': ticket.requester_email,
                    'requester_type': ticket.requester_type,
                    'requester_id': str(ticket.requester_id),
                    'status': ticket.status,
                    'priority': ticket.priority,
                    'category': ticket.category,
                    'assigned_to': {
                        'id': str(ticket.assigned_to.id),
                        'username': ticket.assigned_to.username,
                        'email': ticket.assigned_to.email
                    } if ticket.assigned_to else None,
                    'created_at': ticket.created_at.isoformat(),
                    'updated_at': ticket.updated_at.isoformat(),
                    'resolved_at': ticket.resolved_at.isoformat() if ticket.resolved_at else None,
                    'attachments': ticket.attachments
                },
                'messages': [{
                    'id': str(msg.id),
                    'message_type': msg.message_type,
                    'author_name': msg.author_name,
                    'author_email': msg.author_email,
                    'content': msg.content,
                    'is_internal': msg.is_internal,
                    'created_at': msg.created_at.isoformat(),
                    'attachments': msg.attachments
                } for msg in messages],
                'activities': [{
                    'id': str(activity.id),
                    'activity_type': activity.activity_type,
                    'description': activity.description,
                    'actor_name': activity.actor_name,
                    'actor_type': activity.actor_type,
                    'old_value': activity.old_value,
                    'new_value': activity.new_value,
                    'created_at': activity.created_at.isoformat()
                } for activity in activities]
            })
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            
            # Mettre à jour les champs modifiables
            old_values = {}
            
            if 'priority' in data and data['priority'] != ticket.priority:
                old_values['priority'] = ticket.priority
                ticket.priority = data['priority']
                
                # Enregistrer l'activité
                TicketActivity.objects.create(
                    ticket=ticket,
                    activity_type='priority_changed',
                    description=f"Priorité changée de {old_values['priority']} à {ticket.priority}",
                    actor_id=admin.id,
                    actor_name=admin.username,
                    actor_type='admin',
                    old_value=old_values['priority'],
                    new_value=ticket.priority
                )
            
            if 'category' in data:
                ticket.category = data['category']
            
            ticket.save()
            
            return Response({'message': 'Ticket mis à jour avec succès'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assign_ticket(request, ticket_id):
    """Assigner un ticket à un admin"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        data = json.loads(request.body)
        
        assigned_admin_id = data.get('admin_id')
        if assigned_admin_id:
            assigned_admin = get_object_or_404(AdminUser, id=assigned_admin_id)
        else:
            assigned_admin = admin  # S'assigner le ticket
        
        old_assigned = ticket.assigned_to
        ticket.assigned_to = assigned_admin
        ticket.save()
        
        # Enregistrer l'activité
        TicketActivity.objects.create(
            ticket=ticket,
            activity_type='assigned',
            description=f"Ticket assigné à {assigned_admin.username}",
            actor_id=admin.id,
            actor_name=admin.username,
            actor_type='admin',
            old_value=old_assigned.username if old_assigned else 'Non assigné',
            new_value=assigned_admin.username
        )
        
        return Response({'message': 'Ticket assigné avec succès'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_ticket_status(request, ticket_id):
    """Mettre à jour le statut d'un ticket"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        data = json.loads(request.body)
        
        old_status = ticket.status
        new_status = data.get('status')
        
        if new_status not in dict(SupportTicket.STATUS_CHOICES):
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        ticket.status = new_status
        
        # Si le ticket est résolu, enregistrer la date
        if new_status == 'resolved' and old_status != 'resolved':
            ticket.resolved_at = timezone.now()
        
        ticket.save()
        
        # Enregistrer l'activité
        TicketActivity.objects.create(
            ticket=ticket,
            activity_type='status_changed',
            description=f"Statut changé de {old_status} à {new_status}",
            actor_id=admin.id,
            actor_name=admin.username,
            actor_type='admin',
            old_value=old_status,
            new_value=new_status
        )
        
        return Response({'message': 'Statut mis à jour avec succès'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ticket_messages(request, ticket_id):
    """Messages d'un ticket"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        messages = TicketMessage.objects.filter(ticket=ticket).order_by('created_at')
        
        return Response({
            'messages': [{
                'id': str(msg.id),
                'message_type': msg.message_type,
                'author_name': msg.author_name,
                'author_email': msg.author_email,
                'content': msg.content,
                'is_internal': msg.is_internal,
                'created_at': msg.created_at.isoformat(),
                'attachments': msg.attachments
            } for msg in messages]
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_ticket_message(request, ticket_id):
    """Ajouter un message à un ticket"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        data = json.loads(request.body)
        
        message = TicketMessage.objects.create(
            ticket=ticket,
            message_type='admin_response',
            author_id=admin.id,
            author_name=admin.username,
            author_email=admin.email,
            content=data.get('content', ''),
            is_internal=data.get('is_internal', False),
            attachments=data.get('attachments', [])
        )
        
        # Mettre à jour le statut du ticket si nécessaire
        if not data.get('is_internal', False):
            if ticket.status == 'open':
                ticket.status = 'in_progress'
                ticket.save()
        
        # Enregistrer l'activité
        TicketActivity.objects.create(
            ticket=ticket,
            activity_type='message_added',
            description=f"{'Note interne' if data.get('is_internal') else 'Réponse'} ajoutée par {admin.username}",
            actor_id=admin.id,
            actor_name=admin.username,
            actor_type='admin'
        )
        
        return Response({
            'message': 'Message ajouté avec succès',
            'ticket_message': {
                'id': str(message.id),
                'content': message.content,
                'is_internal': message.is_internal,
                'created_at': message.created_at.isoformat()
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def create_support_ticket(request):
    """Créer un ticket de support (API publique)"""
    try:
        data = json.loads(request.body)
        
        # Validation des données requises
        required_fields = ['requester_type', 'requester_id', 'requester_email', 'requester_name', 'subject', 'description']
        for field in required_fields:
            if not data.get(field):
                return Response({'error': f'Le champ {field} est requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer le ticket
        ticket = SupportTicket.objects.create(
            requester_type=data['requester_type'],
            requester_id=data['requester_id'],
            requester_email=data['requester_email'],
            requester_name=data['requester_name'],
            subject=data['subject'],
            description=data['description'],
            category=data.get('category', 'other'),
            priority=data.get('priority', 'medium'),
            attachments=data.get('attachments', [])
        )
        
        # Créer le message initial
        TicketMessage.objects.create(
            ticket=ticket,
            message_type='user_message',
            author_id=data['requester_id'],
            author_name=data['requester_name'],
            author_email=data['requester_email'],
            content=data['description'],
            attachments=data.get('attachments', [])
        )
        
        # Enregistrer l'activité
        TicketActivity.objects.create(
            ticket=ticket,
            activity_type='created',
            description=f"Ticket créé par {data['requester_name']}",
            actor_id=data['requester_id'],
            actor_name=data['requester_name'],
            actor_type=data['requester_type']
        )
        
        return Response({
            'message': 'Ticket créé avec succès',
            'ticket': {
                'id': str(ticket.id),
                'ticket_number': ticket.ticket_number,
                'status': ticket.status
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_tickets(request, user_id):
    """Tickets d'un utilisateur spécifique"""
    try:
        tickets = SupportTicket.objects.filter(requester_id=user_id).order_by('-created_at')
        
        return Response({
            'tickets': [{
                'id': str(ticket.id),
                'ticket_number': ticket.ticket_number,
                'subject': ticket.subject,
                'status': ticket.status,
                'priority': ticket.priority,
                'category': ticket.category,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat()
            } for ticket in tickets]
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_management(request):
    """Gestion des utilisateurs"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Récupérer les utilisateurs depuis le service auth
        try:
            response = requests.get('http://localhost:8001/api/auth/users/')
            if response.status_code == 200:
                users = response.json()
            else:
                users = []
        except:
            users = []
        
        return Response({'users': users})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def seller_management(request):
    """Gestion des vendeurs"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Récupérer les vendeurs depuis le service seller
        try:
            response = requests.get('http://localhost:8005/api/sellers/')
            if response.status_code == 200:
                sellers = response.json()
            else:
                sellers = []
        except:
            sellers = []
        
        return Response({'sellers': sellers})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def admin_management(request):
    """Gestion des administrateurs"""
    try:
        admin = get_admin_from_token(request)
        if not admin or not admin.is_super_admin:
            return Response({'error': 'Accès refusé'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'GET':
            admins = AdminUser.objects.all()
            return Response({
                'admins': [{
                    'id': str(a.id),
                    'username': a.username,
                    'email': a.email,
                    'role': a.role,
                    'department': a.department,
                    'is_super_admin': a.is_super_admin,
                    'is_active': a.is_active,
                    'created_at': a.created_at.isoformat()
                } for a in admins]
            })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            
            new_admin = AdminUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=data.get('role', 'admin'),
                department=data.get('department', ''),
                is_super_admin=data.get('is_super_admin', False)
            )
            
            return Response({
                'message': 'Administrateur créé avec succès',
                'admin_id': str(new_admin.id)
            }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def get_admin_from_token(request):
    """Récupérer l'admin depuis le token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        token_string = auth_header.split(' ')[1]
        return token_service.validate_admin_token(token_string)
    except:
        return None