# Gmail SMTP Setup for TechSavvy Store

## Overview
Your TechSavvy Store accounts system is **fully functional** with model-based verification! 🎉

✅ **What's Working:**
- 4-digit verification codes (2.5-minute expiry)
- Email verification flow
- Password reset flow  
- User activation system
- Professional email templates

⚠️ **What Needs Setup:**
- Gmail SMTP authentication (to send real emails)

## Gmail App Password Setup

To send real emails to `rings9619@gmail.com`, follow these steps:

### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification if not already enabled
3. This is required for App Passwords

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Other (custom name)" as device
4. Enter "TechSavvy Store" as the name
5. Click "Generate"
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update .env File
Replace the placeholder values in `.env`:

```env
# Email Configuration (Gmail SMTP)
EMAIL_HOST_USER=rings9619@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password-here
```

**Example:**
```env
EMAIL_HOST_USER=rings9619@gmail.com  
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

## Testing Real Email Sending

After setting up the App Password, run:

```bash
python manage.py shell
```

Then test:
```python
from django.core.mail import send_mail
from accounts.utils import send_verification_email

# Test basic Django email
send_mail(
    'Test Email',
    'This is a test email from TechSavvy Store.',
    'rings9619@gmail.com',
    ['rings9619@gmail.com'],
)

# Test our verification email
send_verification_email('rings9619@gmail.com', '1234', {'user_name': 'Test User'})
```

## Complete Flow Test

Once Gmail is configured, test the complete flow:

```bash
# 1. Start the server
python manage.py runserver

# 2. Register a new user (this will send real email!)
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rings9619@gmail.com",
    "username": "testuser123", 
    "password": "Africa123!",
    "confirm_password": "Africa123!",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "1234567890"
  }'

# 3. Check your Gmail inbox for the 4-digit code
# 4. Verify email with the received code
curl -X POST http://localhost:8000/api/accounts/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rings9619@gmail.com",
    "verification_code": "YOUR-4-DIGIT-CODE"
  }'

# 5. Login with verified account
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rings9619@gmail.com",
    "password": "Africa123!"
  }'
```

## API Endpoints

Your accounts system now provides these endpoints:

- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/verify-email/` - Email verification  
- `POST /api/accounts/resend-verification/` - Resend verification code
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/password-reset/` - Request password reset
- `POST /api/accounts/password-reset-confirm/` - Confirm password reset
- `GET /api/accounts/profile/` - Get current user profile

## Email Templates

Professional email templates are located in:
- `templates/emails/verification_email.html` - Verification email (HTML)
- `templates/emails/verification_email.txt` - Verification email (Text)
- `templates/emails/password_reset.html` - Password reset email (HTML)
- `templates/emails/password_reset.txt` - Password reset email (Text)

## Security Features

✅ **Built-in Security:**
- 4-digit codes expire in 2.5 minutes
- Users are inactive until email verified
- Password validation with Django standards
- Rate limiting for email sending
- Security logging for login attempts
- JWT token authentication
- Professional error handling

## Troubleshooting

**"Username and Password not accepted" error:**
- Make sure you're using the **App Password**, not your regular Gmail password
- Ensure 2-Factor Authentication is enabled on your Google account
- Check that the App Password has no spaces (remove them)

**"Connection refused" error:**
- Check that your internet connection allows SMTP on port 587
- Some networks block SMTP, try a different network

**No email received:**
- Check spam/junk folder
- Verify the email address is correct
- Check Gmail's "All Mail" folder

## Production Deployment

For production, consider:
1. Use a dedicated email service (SendGrid, Mailgun, SES)
2. Set up proper DNS records (SPF, DKIM, DMARC)
3. Use environment variables for all sensitive data
4. Enable HTTPS for all API endpoints
5. Set up proper logging and monitoring

---

🎉 **Your TechSavvy Store accounts system is ready!**

The system is fully functional and follows E-LearningSystem patterns with:
- Model-based verification (no external dependencies)
- 4-digit codes with 2.5-minute expiry
- Professional email templates
- Complete authentication flow
- Django best practices