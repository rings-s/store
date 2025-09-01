# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid



class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)  # Require email verification
        extra_fields.setdefault('is_verified', False)  # Start unverified
        extra_fields.setdefault('role', 'customer')
        return self._create_user(email, username, password, **extra_fields)
    
    def create_vendor(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'vendor')
        return self._create_user(email, username, password, **extra_fields)
    
    def create_staff(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Staff user must have is_staff=True.'))
        
        return self._create_user(email, username, password, **extra_fields)
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self._create_user(email, username, password, **extra_fields)
    
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # Address fields
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Additional fields
    loyalty_points = models.IntegerField(default=0)
    preferred_currency = models.CharField(max_length=3, default='USD')
    language_preference = models.CharField(max_length=10, default='en')
    
    # Email verification fields (inspired by E-LearningSystem)
    is_verified = models.BooleanField(default=False, verbose_name=_('Email Verified'))
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name=_('Verification Code'))
    verification_code_created = models.DateTimeField(null=True, blank=True, verbose_name=_('Verification Code Created'))
    reset_code = models.CharField(max_length=6, blank=True, null=True, verbose_name=_('Reset Code'))
    reset_code_created = models.DateTimeField(null=True, blank=True, verbose_name=_('Reset Code Created'))
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        return self.first_name or self.username
    
    @property
    def is_vendor(self):
        return self.role == 'vendor'
    
    @property
    def is_admin(self):
        return self.role in ['admin', 'superadmin']
    
    # E-LearningSystem inspired verification methods
    def generate_verification_code(self, length=4):
        """Generate verification code for email verification"""
        import random
        code = str(random.randint(10**(length-1), 10**length-1))
        self.verification_code = code
        self.verification_code_created = timezone.now()
        self.is_verified = False
        self.save(update_fields=['verification_code', 'verification_code_created', 'is_verified'])
        return code

    def verify_account(self, code):
        """Verify account using verification code"""
        if not self.verification_code or not self.verification_code_created or self.verification_code != code:
            return False
        
        # Check if code has expired (2.5 minutes for store vs 24 hours in E-Learning)
        expiry_time = self.verification_code_created + timezone.timedelta(minutes=2.5)
        if timezone.now() > expiry_time:
            return False

        self.is_verified = True
        self.is_active = True  # Activate user upon verification
        self.verification_code = None
        self.verification_code_created = None
        self.save(update_fields=['is_verified', 'is_active', 'verification_code', 'verification_code_created'])
        return True

    def generate_reset_code(self, length=4):
        """Generate password reset code"""
        import random
        code = str(random.randint(10**(length-1), 10**length-1))
        self.reset_code = code
        self.reset_code_created = timezone.now()
        self.save(update_fields=['reset_code', 'reset_code_created'])
        return code

    def reset_password(self, code, new_password):
        """Reset password using reset code"""
        if not self.reset_code or not self.reset_code_created or self.reset_code != code:
            return False
        
        # Check if code has expired (2.5 minutes for store vs 1 hour in E-Learning)
        expiry_time = self.reset_code_created + timezone.timedelta(minutes=2.5)
        if timezone.now() > expiry_time:
            return False

        self.set_password(new_password)
        self.reset_code = None
        self.reset_code_created = None
        self.save(update_fields=['password', 'reset_code', 'reset_code_created'])
        return True


