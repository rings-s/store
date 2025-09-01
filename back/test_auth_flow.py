#!/usr/bin/env python3
"""
Test authentication flow for the TechSavvy Store accounts system.
Tests the complete flow: registration → email verification → login
"""

import os
import sys
import requests
import json
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
django.setup()

from accounts.models import User

BASE_URL = "http://localhost:8000/api/accounts/"

def test_registration():
    """Test user registration"""
    print("🔸 Testing user registration...")
    
    # First, clean up any existing test user
    try:
        existing_user = User.objects.get(email="rings9619@gmail.com")
        existing_user.delete()
        print("  ♻️ Cleaned up existing test user")
    except User.DoesNotExist:
        pass
    
    registration_data = {
        "email": "rings9619@gmail.com",
        "username": "testuser123",
        "password": "Africa123!",
        "confirm_password": "Africa123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}register/", json=registration_data, timeout=10)
        print(f"  📤 Registration response status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"  ✅ Registration successful!")
            print(f"  📧 User email: {data.get('data', {}).get('email')}")
            return True
        else:
            print(f"  ❌ Registration failed: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ⏰ Registration request timed out")
        return False
    except Exception as e:
        print(f"  ❌ Registration error: {str(e)}")
        return False

def check_user_created():
    """Check if user was created in database"""
    print("\n🔸 Checking user creation in database...")
    
    try:
        user = User.objects.get(email="rings9619@gmail.com")
        print(f"  ✅ User found in database!")
        print(f"  📊 User details:")
        print(f"    - Email: {user.email}")
        print(f"    - Username: {user.username}")
        print(f"    - Is Active: {user.is_active}")
        print(f"    - Is Verified: {user.is_verified}")
        print(f"    - Verification Code: {user.verification_code}")
        
        return user
    except User.DoesNotExist:
        print("  ❌ User not found in database")
        return None

def test_email_verification(user):
    """Test email verification"""
    print("\n🔸 Testing email verification...")
    
    if not user or not user.verification_code:
        print("  ❌ No verification code available")
        return False
    
    verification_data = {
        "email": "rings9619@gmail.com",
        "verification_code": user.verification_code
    }
    
    try:
        response = requests.post(f"{BASE_URL}verify-email/", json=verification_data, timeout=10)
        print(f"  📤 Verification response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Email verification successful!")
            if 'data' in data and 'tokens' in data['data']:
                print(f"  🎟️ Access token received")
                return data['data']['tokens']['access']
            return True
        else:
            print(f"  ❌ Email verification failed: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ⏰ Verification request timed out")
        return False
    except Exception as e:
        print(f"  ❌ Verification error: {str(e)}")
        return False

def test_login():
    """Test user login"""
    print("\n🔸 Testing user login...")
    
    login_data = {
        "email": "rings9619@gmail.com",
        "password": "Africa123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}login/", json=login_data, timeout=10)
        print(f"  📤 Login response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Login successful!")
            print(f"  🎟️ Access token received")
            return data.get('access')
        else:
            print(f"  ❌ Login failed: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ⏰ Login request timed out")
        return False
    except Exception as e:
        print(f"  ❌ Login error: {str(e)}")
        return False

def main():
    """Run the complete authentication flow test"""
    print("🚀 TechSavvy Store Authentication Flow Test")
    print("=" * 50)
    
    # Start Django development server in the background
    import subprocess
    import time
    
    print("🔸 Starting Django development server...")
    server_process = subprocess.Popen([
        sys.executable, "manage.py", "runserver", "localhost:8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test the complete flow
        registration_success = test_registration()
        
        if registration_success:
            user = check_user_created()
            
            if user:
                verification_success = test_email_verification(user)
                
                if verification_success:
                    login_success = test_login()
                    
                    if login_success:
                        print("\n🎉 Complete authentication flow test PASSED!")
                        print("✅ Registration → Email Verification → Login: ALL WORKING")
                        return True
        
        print("\n❌ Authentication flow test FAILED")
        return False
        
    finally:
        # Clean up server process
        print("\n🔸 Stopping Django development server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)