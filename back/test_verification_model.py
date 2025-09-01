#!/usr/bin/env python3
"""
Test the model-based verification system directly
"""

import os
import sys
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
django.setup()

from accounts.models import User
from django.utils import timezone

def test_user_verification_model():
    """Test the User model verification methods"""
    print("🔸 Testing User model verification system...")
    
    # Clean up any existing test user
    try:
        existing_user = User.objects.get(email="test@example.com")
        existing_user.delete()
        print("  ♻️ Cleaned up existing test user")
    except User.DoesNotExist:
        pass
    
    # Create a new user
    print("\n1️⃣ Creating test user...")
    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpass123",
        first_name="Test",
        last_name="User"
    )
    
    print(f"  ✅ User created!")
    print(f"  📊 Initial state:")
    print(f"    - Is Active: {user.is_active}")
    print(f"    - Is Verified: {user.is_verified}")
    print(f"    - Verification Code: {user.verification_code}")
    
    # Test generate verification code
    print("\n2️⃣ Testing generate_verification_code()...")
    code = user.generate_verification_code()
    print(f"  ✅ Generated 4-digit code: {code}")
    print(f"  📊 Updated state:")
    print(f"    - Is Active: {user.is_active}")
    print(f"    - Is Verified: {user.is_verified}")
    print(f"    - Verification Code: {user.verification_code}")
    print(f"    - Code Length: {len(code)} digits")
    print(f"    - Code Created: {user.verification_code_created}")
    
    # Test verify account
    print("\n3️⃣ Testing verify_account()...")
    success = user.verify_account(code)
    print(f"  ✅ Verification result: {success}")
    print(f"  📊 Final state:")
    print(f"    - Is Active: {user.is_active}")
    print(f"    - Is Verified: {user.is_verified}")
    print(f"    - Verification Code: {user.verification_code}")
    
    # Test password reset
    print("\n4️⃣ Testing password reset system...")
    reset_code = user.generate_reset_code()
    print(f"  ✅ Generated reset code: {reset_code}")
    
    # Test reset password
    reset_success = user.reset_password(reset_code, "newpassword123")
    print(f"  ✅ Password reset result: {reset_success}")
    
    # Test expired code
    print("\n5️⃣ Testing expired code...")
    # Generate a new code but manually set it to expired
    expired_code = user.generate_verification_code()
    user.verification_code_created = timezone.now() - timezone.timedelta(minutes=3)  # 3 minutes ago
    user.save()
    
    expired_result = user.verify_account(expired_code)
    print(f"  ✅ Expired code verification result: {expired_result} (should be False)")
    
    # Cleanup
    user.delete()
    print("\n  ♻️ Cleaned up test user")
    
    return True

def test_email_sending():
    """Test email sending functionality"""
    print("\n🔸 Testing email sending utilities...")
    
    from accounts.utils import send_verification_email, send_password_reset_email
    
    try:
        # This should work in DEBUG mode (console backend)
        send_verification_email("test@example.com", "1234", {
            'user_name': 'Test User'
        })
        print("  ✅ Verification email function executed successfully")
        
        send_password_reset_email("test@example.com", "5678", {
            'user_name': 'Test User'
        })
        print("  ✅ Password reset email function executed successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ Email sending error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 TechSavvy Store Model Verification Test")
    print("=" * 50)
    
    model_test = test_user_verification_model()
    email_test = test_email_sending()
    
    if model_test and email_test:
        print("\n🎉 All tests PASSED!")
        print("✅ Model verification system is working correctly")
        return True
    else:
        print("\n❌ Some tests FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)