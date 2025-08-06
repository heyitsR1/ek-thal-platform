import requests
import json
from django.conf import settings
from .models import Profile

class WhatsAppNotifier:
    def __init__(self):
        self.api_url = getattr(settings, 'WHATSAPP_API_URL', None)
        self.api_key = getattr(settings, 'WHATSAPP_API_KEY', None)
        self.phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', None)
        self.admin_phone = getattr(settings, 'ADMIN_WHATSAPP_NUMBER', None)
        
    def send_message(self, phone_number, message):
        """Send WhatsApp message to a specific phone number"""
        if not all([self.api_url, self.api_key, self.phone_number_id]):
            print("WhatsApp API not configured. Skipping message.")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'text',
            'text': {'body': message}
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                headers=headers,
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"WhatsApp API error: {e}")
            return False
    
    def notify_admin_new_listing(self, listing):
        """Notify admin about new pending listing"""
        if not self.admin_phone:
            return False
            
        message = f"""🍽️ NEW FOOD LISTING PENDING APPROVAL

📝 Title: {listing.title}
📍 Location: {listing.location}
⚖️ Quantity: {listing.quantity} kg
👤 Donor: {listing.donor.user.username}
📞 Contact: {listing.donor.phone_number_1}

🔗 Review: https://ekthal.up.railway.app/dashboard/approve-listing/{listing.id}/

⚠️ Please review and approve/reject this listing."""
        
        return self.send_message(self.admin_phone, message)
    
    def notify_receivers_new_listing(self, listing):
        """Notify all receivers about new approved listing"""
        # Get all receiver profiles
        receivers = Profile.objects.filter(is_receiver=True)
        
        message = f"""🍽️ NEW FOOD AVAILABLE!

📝 {listing.title}
📍 {listing.location}
⚖️ {listing.quantity} kg
⏰ Prepared: {listing.prepared_at.strftime('%Y-%m-%d %H:%M') if listing.prepared_at else 'N/A'}

🔗 View: https://ekthal.up.railway.app/listing/{listing.id}/

🚨 Food spoils quickly - claim fast!"""
        
        success_count = 0
        for receiver in receivers:
            if receiver.phone_number_1:
                if self.send_message(receiver.phone_number_1, message):
                    success_count += 1
        
        return success_count
    
    def notify_donor_listing_approved(self, listing):
        """Notify donor when their listing is approved"""
        donor_phone = listing.donor.phone_number_1
        if not donor_phone:
            return False
            
        message = f"""✅ YOUR LISTING HAS BEEN APPROVED!

📝 {listing.title}
📍 {listing.location}
⚖️ {listing.quantity} kg

🎉 Your food listing is now visible to receivers and can be claimed!

🔗 View: https://ekthal.up.railway.app/listing/{listing.id}/"""
        
        return self.send_message(donor_phone, message)
    
    def notify_claim_made(self, claimed_listing):
        """Notify donor when their listing is claimed"""
        donor_phone = claimed_listing.food_listing.donor.phone_number_1
        if not donor_phone:
            return False
            
        message = f"""🎯 YOUR FOOD HAS BEEN CLAIMED!

📝 {claimed_listing.food_listing.title}
👤 Claimed by: {claimed_listing.organization.user.username}
📞 Contact: {claimed_listing.organization.phone_number_1}
⏰ Claimed at: {claimed_listing.claimed_at.strftime('%Y-%m-%d %H:%M')}

🔗 View connection: http://127.0.0.1:8000/connection/{claimed_listing.id}/"""
        
        return self.send_message(donor_phone, message)

# Global instance
whatsapp = WhatsAppNotifier() 