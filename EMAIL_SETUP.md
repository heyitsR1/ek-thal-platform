# Email Notification Setup Guide

## 🚀 Overview

This guide will help you set up email notifications for your food donation platform. The system will send real-time email notifications to:

1. **Admin** - When new food listings are submitted (for approval)
2. **Receivers** - When new food listings are approved
3. **Donors** - When their listings are approved, rejected, or claimed

## 📋 Prerequisites

- A Gmail account (or other SMTP provider)
- Gmail App Password (for Gmail users)
- Admin email address

## 🔧 Setup Steps

### Step 1: Gmail App Password Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Copy the 16-character password

### Step 2: Configure Django Settings

Edit `ekthal/settings.py` and update the email configuration:

```python
# Email Configuration
DEFAULT_FROM_EMAIL = "noreply@ekthal.com"
ADMINS = [
    ("Admin", "your-admin-email@gmail.com"),
]

# Email Backend Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
```

### Step 3: Test the Configuration

Run the test script:

```bash
python test_email.py
```

### Step 4: For Development/Testing

If you want to see emails in the console instead of sending them:

```python
# In settings.py, comment out SMTP and uncomment console backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 📧 Email Templates

The system sends these types of emails:

### 1. Admin Notification (New Listing)
```
Subject: 🍽️ New Food Listing Pending Approval - EkThal

Hello Admin,

A new food listing has been submitted and requires your approval.

📝 LISTING DETAILS:
• Title: Fresh Bread
• Location: Kathmandu, Nepal
• Quantity: 5 kg
• Type: Bakery
• Prepared At: 2024-01-15 14:30
• Storage: Room Temperature
• Prepared By: Home

👤 DONOR INFORMATION:
• Username: john_doe
• Email: john@example.com
• Phone 1: +9771234567890
• Phone 2: Not provided
• Organization: No

📄 DESCRIPTION:
Fresh homemade bread made this morning.

📋 SPECIAL INSTRUCTIONS:
None

🔗 REVIEW LINK:
http://127.0.0.1:8000/dashboard/approve-listing/123/

⚠️ Please review and approve/reject this listing as soon as possible.

Best regards,
EkThal Team
```

### 2. Receiver Notification (New Available Food)
```
Subject: 🍽️ New Food Available - EkThal

Hello Food Receiver,

Great news! A new food listing has been approved and is now available for claiming.

📝 FOOD DETAILS:
• Title: Fresh Vegetables
• Location: Kathmandu, Nepal
• Quantity: 3 kg
• Type: Vegetables
• Prepared At: 2024-01-15 14:30
• Storage: Refrigerated

📄 DESCRIPTION:
Fresh organic vegetables from local farm.

📋 SPECIAL INSTRUCTIONS:
None

🔗 VIEW LISTING:
http://127.0.0.1:8000/listing/123/

🚨 IMPORTANT: Food spoils quickly! Please claim this listing as soon as possible if you're interested.

Best regards,
EkThal Team
```

### 3. Donor Notification (Listing Approved)
```
Subject: ✅ Your Food Listing Has Been Approved - EkThal

Hello john_doe,

Great news! Your food listing has been approved and is now visible to all receivers.

📝 YOUR LISTING:
• Title: Fresh Bread
• Location: Kathmandu, Nepal
• Quantity: 5 kg
• Type: Bakery

🎉 Your food listing is now live and can be claimed by receivers!

🔗 VIEW YOUR LISTING:
http://127.0.0.1:8000/listing/123/

Thank you for contributing to reducing food waste and helping those in need.

Best regards,
EkThal Team
```

### 4. Donor Notification (Food Claimed)
```
Subject: 🎯 Your Food Has Been Claimed - EkThal

Hello john_doe,

Great news! Your food listing has been claimed by a receiver.

📝 CLAIMED LISTING:
• Title: Fresh Bread
• Location: Kathmandu, Nepal
• Quantity: 5 kg

👤 CLAIMED BY:
• Organization: charity_org
• Contact: +9779876543210
• Email: charity@example.com

⏰ CLAIMED AT: 2024-01-15 15:30

🔗 VIEW CONNECTION:
http://127.0.0.1:8000/connection/456/

Please coordinate with the receiver for food pickup/delivery.

Thank you for your contribution to reducing food waste!

Best regards,
EkThal Team
```

## 🔒 Security Considerations

1. **App Passwords**: Never use your regular Gmail password
2. **Environment Variables**: For production, use environment variables:

```python
import os

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
```

3. **Rate Limiting**: Be aware of Gmail's sending limits (500/day for regular accounts)

## 🚨 Troubleshooting

### Common Issues:

1. **"Authentication failed"**: Check your app password
2. **"Connection refused"**: Check EMAIL_HOST and EMAIL_PORT
3. **"No emails sent"**: Check console for error messages
4. **"Gmail blocking"**: Enable "Less secure app access" or use app passwords

### Testing:

```bash
# Test configuration
python test_email.py

# Check logs
python manage.py runserver
# Look for email-related print statements
```

## 💰 Cost Estimation

Email notifications are **FREE** with Gmail:
- **Gmail**: 500 emails/day (free)
- **Gmail Business**: 2000 emails/day (free)
- **Other providers**: Varies

## 📞 Alternative SMTP Providers

### Gmail (Recommended)
- **Pros**: Free, reliable, easy setup
- **Cons**: 500 emails/day limit
- **Setup**: Use app passwords

### SendGrid
- **Pros**: 100 emails/day free, good for scaling
- **Cons**: Requires signup
- **Setup**: API key authentication

### Mailgun
- **Pros**: 5000 emails/month free
- **Cons**: Requires domain verification
- **Setup**: API key authentication

## 🎯 Next Steps

1. **Choose your email provider** (Gmail recommended for MVP)
2. **Set up app password** (for Gmail)
3. **Configure settings.py** with your credentials
4. **Test with the provided script**
5. **Deploy and monitor email delivery**
6. **Consider email templates for production**

## 🔧 Production Setup

For production deployment:

1. **Use environment variables** for sensitive data
2. **Set up proper domain** in email settings
3. **Configure SPF/DKIM** for better deliverability
4. **Monitor email logs** for delivery issues
5. **Set up email templates** with your branding

---

**Note**: This implementation provides reliable email notifications that work immediately without external API dependencies. Perfect for hackathon MVPs and production deployments! 