from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
import uuid

class UserProfile(models.Model):
    """
    Perfil extendido de usuario
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('researcher', 'Researcher'),
        ('viewer', 'Viewer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    
    # Campos para verificación de email
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def generate_email_verification_token(self):
        """Generar token único para verificación de email"""
        self.email_verification_token = str(uuid.uuid4())
        self.email_verification_sent_at = timezone.now()
        self.save()
        return self.email_verification_token
    
    def send_email_verification(self):
        """Enviar email de verificación"""
        token = self.generate_email_verification_token()
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        subject = 'Verifica tu cuenta - BGBM System'
        message = f"""
Hola {self.user.first_name or self.user.username},

¡Gracias por registrarte en el sistema BGBM!

Para completar tu registro, por favor verifica tu dirección de email haciendo clic en el siguiente enlace:
{verification_url}

Si no te registraste en nuestro sistema, puedes ignorar este email.

El enlace expira en 24 horas.

Saludos,
Equipo BGBM
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error enviando email de verificación: {str(e)}")
            return False
    
    def verify_email_token(self, token):
        """Verificar token de email"""
        if self.email_verification_token == token:
            # Verificar que no haya expirado (24 horas)
            if self.email_verification_sent_at:
                expiry_time = self.email_verification_sent_at + timezone.timedelta(hours=24)
                if timezone.now() <= expiry_time:
                    self.email_verified = True
                    self.user.is_active = True
                    self.email_verification_token = None
                    self.email_verification_sent_at = None
                    self.save()
                    self.user.save()
                    return True
        return False

# Señales para crear automáticamente token y perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    """Crear token automáticamente cuando se crea un usuario"""
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crear perfil automáticamente cuando se crea un usuario"""
    if created:
        # Usuario inactivo hasta verificar email
        instance.is_active = False
        instance.save()
        
        profile = UserProfile.objects.create(user=instance)
        # Enviar email de verificación automáticamente
        profile.send_email_verification()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guardar perfil cuando se guarda el usuario"""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)