from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class AdminUser(AbstractUser):
    """Modèle d'utilisateur admin personnalisé"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, default='admin')
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_users'

class SupportTicket(models.Model):
    """Tickets de support des utilisateurs et vendeurs"""
    TICKET_TYPES = [
        ('user', 'Utilisateur'),
        ('seller', 'Vendeur'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('urgent', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('waiting_response', 'En attente de réponse'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    ]
    
    CATEGORIES = [
        ('account', 'Compte'),
        ('payment', 'Paiement'),
        ('order', 'Commande'),
        ('product', 'Produit'),
        ('technical', 'Technique'),
        ('billing', 'Facturation'),
        ('other', 'Autre'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=20, unique=True)
    
    # Informations du demandeur
    requester_type = models.CharField(max_length=10, choices=TICKET_TYPES)
    requester_id = models.UUIDField()  # ID de l'utilisateur ou vendeur
    requester_email = models.EmailField()
    requester_name = models.CharField(max_length=255)
    
    # Détails du ticket
    subject = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Assignation
    assigned_to = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Fichiers joints
    attachments = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'support_tickets'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Générer un numéro de ticket unique
            import random
            import string
            self.ticket_number = f"TK{''.join(random.choices(string.digits, k=8))}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.subject}"

class TicketMessage(models.Model):
    """Messages dans un ticket de support"""
    MESSAGE_TYPES = [
        ('user_message', 'Message utilisateur'),
        ('admin_response', 'Réponse admin'),
        ('internal_note', 'Note interne'),
        ('system_message', 'Message système'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    
    # Auteur du message
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    author_id = models.UUIDField(null=True, blank=True)  # ID de l'auteur
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField(null=True, blank=True)
    
    # Contenu
    content = models.TextField()
    is_internal = models.BooleanField(default=False)  # Visible seulement par les admins
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Fichiers joints
    attachments = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'ticket_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"Message de {self.author_name} - {self.ticket.ticket_number}"

class TicketActivity(models.Model):
    """Journal d'activité des tickets"""
    ACTIVITY_TYPES = [
        ('created', 'Ticket créé'),
        ('assigned', 'Ticket assigné'),
        ('status_changed', 'Statut modifié'),
        ('priority_changed', 'Priorité modifiée'),
        ('message_added', 'Message ajouté'),
        ('resolved', 'Ticket résolu'),
        ('closed', 'Ticket fermé'),
        ('reopened', 'Ticket rouvert'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='activities')
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    
    # Auteur de l'action
    actor_id = models.UUIDField(null=True, blank=True)
    actor_name = models.CharField(max_length=255)
    actor_type = models.CharField(max_length=20)  # 'admin', 'user', 'seller', 'system'
    
    # Données de l'activité
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_activities'
        ordering = ['-created_at']

class AdminDashboardStats(models.Model):
    """Statistiques pour le dashboard admin"""
    date = models.DateField(unique=True)
    
    # Statistiques des tickets
    total_tickets = models.IntegerField(default=0)
    open_tickets = models.IntegerField(default=0)
    resolved_tickets = models.IntegerField(default=0)
    avg_resolution_time = models.FloatField(default=0)  # en heures
    
    # Statistiques des utilisateurs
    new_users = models.IntegerField(default=0)
    new_sellers = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    total_sellers = models.IntegerField(default=0)
    
    # Statistiques des ventes
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_dashboard_stats'
        ordering = ['-date']