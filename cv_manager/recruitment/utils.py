from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list):
    """
    Envoie un email de notification aux administrateurs.

    :param subject: Sujet de l'email
    :param message: Corps du message
    :param recipient_list: Liste des emails des destinataires
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Doit être configuré dans settings.py
        recipient_list=recipient_list,
        fail_silently=False,  # Active l'affichage des erreurs
    )

def get_admin_emails():
    return [user.email for user in User.objects.filter(is_staff=True, is_active=True) if user.email]