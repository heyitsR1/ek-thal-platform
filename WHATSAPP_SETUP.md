# WhatsApp Business API Setup Guide

## 🚀 Overview

This guide will help you set up WhatsApp Business API notifications for your food donation platform. The system will send real-time notifications to:

1. **Admin** - When new food listings are submitted (for approval)
2. **Receivers** - When new food listings are approved
3. **Donors** - When their listings are approved or claimed

## 📋 Prerequisites

- A business phone number
- Business verification (for most providers)
- Budget for API costs (typically $0.01-0.05 per message)

## 🔧 API Provider Options

### Option 1: 360dialog (Recommended for Startups)
- **Website**: https://www.360dialog.com/
- **Pros**: Easy setup, good documentation, reasonable pricing
- **Cons**: Requires business verification
- **Cost**: ~$0.01-0.03 per message

### Option 2: Twilio WhatsApp API
- **Website**: https://www.twilio.com/whatsapp
- **Pros**: Reliable, good documentation, pay-as-you-go
- **Cons**: Requires phone number verification
- **Cost**: ~$0.005-0.02 per message

### Option 3: MessageBird
- **Website**: https://messagebird.com/
- **Pros**: Simple setup, good for small businesses
- **Cons**: Limited features
- **Cost**: ~$0.01-0.04 per message

## 🛠️ Setup Steps

### Step 1: Choose and Register with Provider

1. **360dialog Setup**:
   - Go to https://www.360dialog.com/
   - Sign up for WhatsApp Business API
   - Complete business verification
   - Get your API credentials

2. **Twilio Setup**:
   - Go to https://www.twilio.com/
   - Sign up and verify your account
   - Enable WhatsApp Sandbox (for testing)
   - Get your Account SID and Auth Token

### Step 2: Configure Django Settings

Edit `ekthal/settings.py` and add your credentials:

```python
# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"  # For 360dialog/Meta
# OR
WHATSAPP_API_URL = "https://api.twilio.com/2010-04-01"  # For Twilio

WHATSAPP_API_KEY = "your_api_key_here"
WHATSAPP_PHONE_NUMBER_ID = "your_phone_number_id"
ADMIN_WHATSAPP_NUMBER = "9771234567890"  # Admin's number with country code
```

### Step 3: Test the Integration

Run the test script:

```bash
python test_whatsapp.py
```

### Step 4: Update Production URLs

Before going live, update the URLs in `app/whatsapp.py`:

```python
# Change from:
"http://127.0.0.1:8000/"

# To your production domain:
"https://yourdomain.com/"
```

## 📱 Message Templates

The system sends these types of messages:

### 1. Admin Notification (New Listing)
```
🍽️ NEW FOOD LISTING PENDING APPROVAL

📝 Title: Fresh Bread
📍 Location: Kathmandu, Nepal
⚖️ Quantity: 5 kg
👤 Donor: john_doe
📞 Contact: +9771234567890

🔗 Review: https://yourdomain.com/dashboard/approve-listing/123/

⚠️ Please review and approve/reject this listing.
```

### 2. Receiver Notification (New Available Food)
```
🍽️ NEW FOOD AVAILABLE!

📝 Fresh Vegetables
📍 Kathmandu, Nepal
⚖️ 3 kg
⏰ Prepared: 2024-01-15 14:30

🔗 View: https://yourdomain.com/listing/123/

🚨 Food spoils quickly - claim fast!
```

### 3. Donor Notification (Listing Approved)
```
✅ YOUR LISTING HAS BEEN APPROVED!

📝 Fresh Bread
📍 Kathmandu, Nepal
⚖️ 5 kg

🎉 Your food listing is now visible to receivers and can be claimed!

🔗 View: https://yourdomain.com/listing/123/
```

### 4. Donor Notification (Food Claimed)
```
🎯 YOUR FOOD HAS BEEN CLAIMED!

📝 Fresh Bread
👤 Claimed by: charity_org
📞 Contact: +9779876543210
⏰ Claimed at: 2024-01-15 15:30

🔗 View connection: https://yourdomain.com/connection/456/
```

## 🔒 Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **Environment Variables**: Use environment variables for production:

```python
import os

WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY')
WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
ADMIN_WHATSAPP_NUMBER = os.environ.get('ADMIN_WHATSAPP_NUMBER')
```

3. **Rate Limiting**: Be aware of API rate limits
4. **Error Handling**: The system gracefully falls back to email if WhatsApp fails

## 💰 Cost Estimation

For a typical food donation platform:

- **100 listings/month**: $1-5
- **500 listings/month**: $5-25
- **1000 listings/month**: $10-50

## 🚨 Troubleshooting

### Common Issues:

1. **"API not configured"**: Check your settings.py configuration
2. **"Message failed"**: Verify phone numbers have country codes
3. **"Rate limit exceeded"**: Implement message queuing for high volume
4. **"Business verification required"**: Complete provider's verification process

### Testing:

```bash
# Test configuration
python test_whatsapp.py

# Check logs
python manage.py runserver
# Look for WhatsApp-related print statements
```

## 📞 Support

- **360dialog**: https://www.360dialog.com/support
- **Twilio**: https://support.twilio.com/
- **MessageBird**: https://support.messagebird.com/

## 🎯 Next Steps

1. Choose your WhatsApp API provider
2. Complete business verification
3. Configure credentials in settings.py
4. Test with the provided script
5. Deploy and monitor message delivery
6. Consider implementing message queuing for high volume

---

**Note**: This implementation includes fallback to email notifications if WhatsApp fails, ensuring your platform remains functional even if there are API issues. 