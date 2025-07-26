from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

class EmailNotifier:
    def __init__(self):
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.admin_emails = [admin[1] for admin in settings.ADMINS]
    
    def send_admin_new_listing_notification(self, listing):
        """Send email to admin about new pending listing"""
        subject = '🍽️ New Food Listing Pending Approval - EkThal'
        
        message = f"""Hello Admin,

A new food listing has been submitted and requires your approval.

📝 LISTING DETAILS:
• Title: {listing.title}
• Location: {listing.location}
• Quantity: {listing.quantity} kg
• Prepared At: {listing.prepared_at.strftime('%Y-%m-%d %H:%M') if listing.prepared_at else 'Not specified'}
• Storage: {listing.storage or 'Not specified'}
• Prepared By: {listing.prepared_by or 'Not specified'}

👤 DONOR INFORMATION:
• Username: {listing.donor.user.username}
• Email: {listing.donor.user.email}
• Phone 1: {listing.donor.phone_number_1}
• Phone 2: {listing.donor.phone_number_2 or 'Not provided'}
• Organization: {'Yes' if listing.donor.is_organization else 'No'}

📄 DESCRIPTION:
{listing.description}

📋 SPECIAL INSTRUCTIONS:
{listing.special_instructions or 'None'}

🔗 REVIEW LINK:
{ settings.SITE_URL }/dashboard/approve-listing/{listing.id}/

⚠️ Please review and approve/reject this listing as soon as possible.

Best regards,
EkThal Team"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=self.admin_emails,
                fail_silently=False,
            )
            print(f"✅ Admin notification email sent for listing {listing.id}")
            return True
        except Exception as e:
            print(f"❌ Failed to send admin notification email: {e}")
            return False
    
    def send_receivers_new_listing_notification(self, listing):
        """Send email to all receivers about new approved listing"""
        # Get all receiver profiles with email addresses
        receivers = Profile.objects.filter(is_receiver=True)
        receiver_emails = []
        
        for receiver in receivers:
            if receiver.user.email:
                receiver_emails.append(receiver.user.email)
        
        if not receiver_emails:
            print("⚠️ No receiver emails found")
            return 0
        
        subject = '🍽️ New Food Available - EkThal'
        
        message = f"""Hello Food Receiver,

Great news! A new food listing has been approved and is now available for claiming.

📝 FOOD DETAILS:
• Title: {listing.title}
• Location: {listing.location}
• Quantity: {listing.quantity} kg
• Prepared At: {listing.prepared_at.strftime('%Y-%m-%d %H:%M') if listing.prepared_at else 'Not specified'}
• Storage: {listing.storage or 'Not specified'}

📄 DESCRIPTION:
{listing.description}

📋 SPECIAL INSTRUCTIONS:
{listing.special_instructions or 'None'}

🔗 VIEW LISTING:
{ settings.SITE_URL }/listing/{listing.id}/

🚨 IMPORTANT: Food spoils quickly! Please claim this listing as soon as possible if you're interested.

Best regards,
EkThal Team"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=receiver_emails,
                fail_silently=False,
            )
            print(f"✅ Notified {len(receiver_emails)} receivers about new listing {listing.id}")
            return len(receiver_emails)
        except Exception as e:
            print(f"❌ Failed to send receiver notification emails: {e}")
            return 0
    
    def send_donor_listing_approved_notification(self, listing):
        """Send email to donor when their listing is approved"""
        donor_email = listing.donor.user.email
        if not donor_email:
            print(f"⚠️ No email found for donor {listing.donor.user.username}")
            return False
        
        subject = '✅ Your Food Listing Has Been Approved - EkThal'
        
        message = f"""Hello {listing.donor.user.username},

Great news! Your food listing has been approved and is now visible to all receivers.

📝 YOUR LISTING:
• Title: {listing.title}
• Location: {listing.location}
• Quantity: {listing.quantity} kg

🎉 Your food listing is now live and can be claimed by receivers!

🔗 VIEW YOUR LISTING:
{ settings.SITE_URL }/listing/{listing.id}/

Thank you for contributing to reducing food waste and helping those in need.

Best regards,
EkThal Team"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[donor_email],
                fail_silently=False,
            )
            print(f"✅ Donor approval notification sent to {donor_email}")
            return True
        except Exception as e:
            print(f"❌ Failed to send donor approval notification: {e}")
            return False
    
    def send_donor_listing_rejected_notification(self, listing, reason=""):
        """Send email to donor when their listing is rejected"""
        donor_email = listing.donor.user.email
        if not donor_email:
            print(f"⚠️ No email found for donor {listing.donor.user.username}")
            return False
        
        subject = '❌ Your Food Listing Has Been Rejected - EkThal'
        
        message = f"""Hello {listing.donor.user.username},

We regret to inform you that your food listing has been rejected by our admin team.

📝 REJECTED LISTING:
• Title: {listing.title}
• Location: {listing.location}
• Quantity: {listing.quantity} kg

{f"📋 REASON: {reason}" if reason else "📋 REASON: No specific reason provided"}

If you have any questions about this decision, please contact our support team.

You can submit a new listing at any time with the necessary corrections.

Best regards,
EkThal Team"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[donor_email],
                fail_silently=False,
            )
            print(f"✅ Donor rejection notification sent to {donor_email}")
            return True
        except Exception as e:
            print(f"❌ Failed to send donor rejection notification: {e}")
            return False
    
    def send_claim_notification_to_donor(self, claimed_listing):
        """Send email to donor when their food is claimed"""
        donor_email = claimed_listing.food_listing.donor.user.email
        if not donor_email:
            print(f"⚠️ No email found for donor {claimed_listing.food_listing.donor.user.username}")
            return False
        
        subject = '🎯 Your Food Has Been Claimed - EkThal'
        
        message = f"""Hello {claimed_listing.food_listing.donor.user.username},

Great news! Your food listing has been claimed by a receiver.

📝 CLAIMED LISTING:
• Title: {claimed_listing.food_listing.title}
• Location: {claimed_listing.food_listing.location}
• Quantity: {claimed_listing.food_listing.quantity} kg

👤 CLAIMED BY:
• Organization: {claimed_listing.organization.user.username}
• Contact: {claimed_listing.organization.phone_number_1}
• Email: {claimed_listing.organization.user.email}

⏰ CLAIMED AT: {claimed_listing.claimed_at.strftime('%Y-%m-%d %H:%M')}

🔗 VIEW CONNECTION:
{ settings.SITE_URL }/connection/{claimed_listing.id}/

Please coordinate with the receiver for food pickup/delivery.

Thank you for your contribution to reducing food waste!

Best regards,
EkThal Team"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[donor_email],
                fail_silently=False,
            )
            print(f"✅ Claim notification sent to donor {donor_email}")
            return True
        except Exception as e:
            print(f"❌ Failed to send claim notification: {e}")
            return False

# Global instance
email_notifier = EmailNotifier() 