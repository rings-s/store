# accounts/utils.py
import secrets
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import hashlib
import jwt
from typing import Optional, Dict, Any


class TokenGenerator:
    @staticmethod
    def generate_token(length: int = 32) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_numeric_otp(length: int = 6) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
    
    @staticmethod
    def generate_jwt_token(payload: Dict[str, Any], expiry_hours: int = 24) -> str:
        payload['exp'] = timezone.now() + timedelta(hours=expiry_hours)
        payload['iat'] = timezone.now()
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class EmailService:
    @staticmethod
    def send_verification_email(user, token):
        subject = 'Verify Your Email - Online Store'
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        context = {
            'user': user,
            'verification_url': verification_url,
            'company_name': 'Online Store',
            'support_email': 'support@onlinestore.com',
            'year': timezone.now().year,
        }
        
        html_message = render_to_string('email/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset_email(user, token):
        subject = 'Password Reset Request - Online Store'
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        context = {
            'user': user,
            'reset_url': reset_url,
            'company_name': 'Online Store',
            'support_email': 'support@onlinestore.com',
            'year': timezone.now().year,
            'expiry_hours': 2,
        }
        
        html_message = render_to_string('email/reset_request.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset_confirmation(user):
        subject = 'Password Successfully Reset - Online Store'
        
        context = {
            'user': user,
            'company_name': 'Online Store',
            'support_email': 'support@onlinestore.com',
            'year': timezone.now().year,
        }
        
        html_message = render_to_string('email/reset_confirm.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_welcome_email(user):
        subject = 'Welcome to Online Store!'
        
        context = {
            'user': user,
            'company_name': 'Online Store',
            'support_email': 'support@onlinestore.com',
            'year': timezone.now().year,
            'dashboard_url': f"{settings.FRONTEND_URL}/dashboard",
        }
        
        html_message = render_to_string('email/welcome.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )


class SecurityUtils:
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def get_user_agent(request):
        return request.META.get('HTTP_USER_AGENT', '')
    
    @staticmethod
    def detect_device_type(user_agent: str) -> str:
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            return 'Mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'Tablet'
        else:
            return 'Desktop'
    
    @staticmethod
    def should_lock_account(failed_attempts: int) -> bool:
        return failed_attempts >= 5
    
    @staticmethod
    def get_lock_duration() -> timedelta:
        return timedelta(minutes=30)
