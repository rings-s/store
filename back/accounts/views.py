# accounts/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer, 
    UserBriefSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer
)
from .utils import (
    send_verification_email, 
    send_password_reset_email,
    create_response
)
import logging

logger = logging.getLogger('accounts')
security_logger = logging.getLogger('security')
User = get_user_model()

# Authentication Views
class LoginView(TokenObtainPairView):
    """Enhanced login view with email verification check"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class RegisterView(generics.CreateAPIView):
    """Enhanced registration view with email verification"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            
            # Generate and send verification code
            verification_code = user.generate_verification_code()
            send_verification_email(user.email, verification_code, {
                'user_name': f"{user.first_name} {user.last_name}",
                'login_url': f"{request.build_absolute_uri('/')[:-1]}/login"
            })
            
            # Log registration
            security_logger.info(
                f"New user registered: {user.email} from {request.META.get('REMOTE_ADDR')}"
            )
            
            return create_response(
                data={'email': user.email},
                message='Registration successful. Please check your email for verification.',
                status_code=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return create_response(
                error="Registration failed. Please try again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

class VerifyEmailView(APIView):
    """Email verification using model-based 4-digit codes"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = EmailVerificationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            code = serializer.validated_data['verification_code']
            
            user = get_object_or_404(User, email=email)
            
            if user.is_verified:
                return create_response(
                    message='Email already verified',
                    status_code=status.HTTP_200_OK
                )
            
            if user.verify_account(code):
                # Generate tokens for immediate login
                refresh = RefreshToken.for_user(user)
                
                # Log verification
                security_logger.info(f"Email verified for user: {email}")
                
                return create_response(
                    data={
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        },
                        'user': UserBriefSerializer(user).data
                    },
                    message='Email verified successfully',
                    status_code=status.HTTP_200_OK
                )
            
            return create_response(
                error='Invalid or expired verification code',
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            return create_response(
                error="Verification failed. Please try again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

class ResendVerificationView(APIView):
    """Resend verification email with rate limiting"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            email = request.data.get('email')
            if not email:
                return create_response(
                    error='Email is required',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            user = get_object_or_404(User, email=email)
            
            if user.is_verified:
                return create_response(
                    message='Email already verified',
                    status_code=status.HTTP_200_OK
                )
            
            # Generate new code and send email
            verification_code = user.generate_verification_code()
            send_verification_email(user.email, verification_code, {
                'user_name': f"{user.first_name} {user.last_name}",
                'login_url': f"{request.build_absolute_uri('/')[:-1]}/login"
            })
            
            return create_response(
                message='Verification email sent',
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Resend verification error: {str(e)}")
            return create_response(
                error="Failed to send verification email. Please try again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetRequestView(APIView):
    """Password reset request with enhanced security"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = PasswordResetRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                reset_code = user.generate_reset_code()
                send_password_reset_email(user.email, reset_code, {
                    'user_name': f"{user.first_name} {user.last_name}",
                    'reset_url': f"{request.build_absolute_uri('/')[:-1]}/reset-password?email={email}&code={reset_code}"
                })
                
                security_logger.info(f"Password reset requested for: {email}")
                
            except User.DoesNotExist:
                # Don't reveal if email exists for security
                pass
            
            return create_response(
                message='If an account exists with this email, password reset instructions have been sent',
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}")
            return create_response(
                error="Failed to process password reset. Please try again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetConfirmView(APIView):
    """Confirm password reset with enhanced validation"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = PasswordResetConfirmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            reset_code = serializer.validated_data['reset_code']
            new_password = serializer.validated_data['new_password']
            
            user = get_object_or_404(User, email=email)
            
            if user.reset_password(reset_code, new_password):
                # Generate new tokens
                refresh = RefreshToken.for_user(user)
                
                # Log password reset
                security_logger.info(f"Password reset completed for: {email}")
                
                return create_response(
                    data={
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    message='Password reset successfully',
                    status_code=status.HTTP_200_OK
                )
            
            return create_response(
                error='Invalid or expired reset code',
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Password reset confirm error: {str(e)}")
            return create_response(
                error="Failed to reset password. Please try again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

# User Management Views
class CurrentUserView(generics.RetrieveAPIView):
    """Get current user profile"""
    serializer_class = UserBriefSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user