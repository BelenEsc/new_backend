from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este nombre de usuario")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # El usuario se crea inactivo hasta verificar email (se maneja en signals)
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer para login de usuarios"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales incorrectas')
            if not user.is_active:
                if hasattr(user, 'userprofile') and not user.userprofile.email_verified:
                    raise serializers.ValidationError('Debes verificar tu email antes de iniciar sesión. Revisa tu bandeja de entrada.')
                raise serializers.ValidationError('Usuario desactivado')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Debe incluir username y password')

class EmailVerificationSerializer(serializers.Serializer):
    """Serializer para verificación de email"""
    token = serializers.CharField()
    
    def validate_token(self, value):
        try:
            profile = UserProfile.objects.get(email_verification_token=value)
            if profile.verify_email_token(value):
                return value
            else:
                raise serializers.ValidationError("Token expirado o inválido")
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Token inválido")

class ResendVerificationSerializer(serializers.Serializer):
    """Serializer para reenviar verificación de email"""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.userprofile.email_verified:
                raise serializers.ValidationError("Este email ya está verificado")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe usuario con este email")
    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        return user.userprofile.send_email_verification()

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil de usuario"""
    email_verified = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('phone', 'department', 'role', 'email_verified')

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalles de usuario"""
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'is_active', 'date_joined', 'profile')

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas nuevas no coinciden")
        return attrs

class PasswordResetSerializer(serializers.Serializer):
    """Serializer para solicitud de reset de contraseña"""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if not user.is_active:
                raise serializers.ValidationError("Usuario inactivo. Verifica tu email primero.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe usuario con este email")
    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generar token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # URL del frontend para reset
        reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
        
        # Enviar email
        subject = 'Recuperación de Contraseña - BGBM System'
        message = f"""
Hola {user.first_name or user.username},

Recibimos una solicitud para recuperar tu contraseña.

Para crear una nueva contraseña, haz clic en el siguiente enlace:
{reset_url}

Si no solicitaste este cambio, puedes ignorar este email.

El enlace expira en 1 hora.

Saludos,
Equipo BGBM
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            raise serializers.ValidationError(f"Error enviando email: {str(e)}")

class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar reset de contraseña"""
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        # Validar token
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=uid)
            
            if not default_token_generator.check_token(user, attrs['token']):
                raise serializers.ValidationError("Token inválido o expirado")
                
            attrs['user'] = user
            return attrs
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Token inválido")
    
    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user