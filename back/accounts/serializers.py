# accounts/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.db import transaction
import logging

logger = logging.getLogger('accounts')
security_logger = logging.getLogger('security')
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Enhanced token serializer with email verification check"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        if 'username' in self.fields:
            del self.fields['username']  # Remove username field if it exists
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        ip_address = request.META.get('REMOTE_ADDR') if request else None
        
        # Authenticate user
        user = authenticate(request=request, email=email, password=password)
        
        if user is None:
            security_logger.warning(
                f"Failed login attempt for {email} from {ip_address}"
            )
            raise serializers.ValidationError(_('Invalid email or password.'))
        
        if not user.is_active:
            security_logger.warning(
                f"Login attempt for inactive user {email} from {ip_address}"
            )
            raise serializers.ValidationError(_('User account is disabled.'))
        
        if not user.is_verified:
            raise serializers.ValidationError(
                _('Email address is not verified. Please check your email.')
            )
        
        # Log successful login
        security_logger.info(f"Successful login for {email} from {ip_address}")
        
        # Call parent validation
        attrs['email'] = email
        attrs['username'] = email  # Use email as username for parent class
        data = super().validate(attrs)
        
        # Add user data to response
        refresh = self.get_token(user)
        data['user'] = UserBriefSerializer(user).data
        
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'confirm_password', 'first_name', 
            'last_name', 'phone_number'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("A user with this email already exists."))
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("A user with this username already exists."))
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('confirm_password', None):
            raise serializers.ValidationError({"confirm_password": _("Passwords do not match.")})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        logger.info(f"New user registered: {user.email}")
        return user

class UserBriefSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'role', 'avatar']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(required=True, min_length=4, max_length=4)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            # Don't reveal if email exists for security
            pass
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    reset_code = serializers.CharField(required=True, min_length=4, max_length=4)
    new_password = serializers.CharField(
        required=True, 
        write_only=True, 
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": _("Passwords do not match.")})
        return attrs