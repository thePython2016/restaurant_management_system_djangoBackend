# tasks.py (Celery tasks)
from celery import shared_task
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings
from .models import SMSCampaign, SMSMessage, Contact
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_bulk_sms(campaign_id):
    try:
        campaign = SMSCampaign.objects.get(id=campaign_id)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Get all unique recipients
        all_recipients = set()
        for contact in campaign.recipients.all():
            all_recipients.add(contact)
        for group in campaign.recipient_groups.all():
            for contact in group.contacts.filter(is_active=True):
                all_recipients.add(contact)
        
        campaign.total_recipients = len(all_recipients)
        campaign.save()
        
        successful_sends = 0
        failed_sends = 0
        
        for recipient in all_recipients:
            try:
                message = client.messages.create(
                    body=campaign.message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=recipient.phone_number
                )
                
                SMSMessage.objects.create(
                    campaign=campaign,
                    recipient=recipient,
                    message_sid=message.sid,
                    status='sent',
                    sent_at=timezone.now()
                )
                successful_sends += 1
                
            except Exception as e:
                SMSMessage.objects.create(
                    campaign=campaign,
                    recipient=recipient,
                    status='failed',
                    error_message=str(e)
                )
                failed_sends += 1
                logger.error(f"Failed to send SMS to {recipient.phone_number}: {e}")
        
        campaign.successful_sends = successful_sends
        campaign.failed_sends = failed_sends
        campaign.status = 'completed'
        campaign.sent_at = timezone.now()
        campaign.save()
        
        logger.info(f"Campaign {campaign.name} completed: {successful_sends} sent, {failed_sends} failed")
        
    except Exception as e:
        logger.error(f"Campaign {campaign_id} failed: {e}")
        campaign.status = 'failed'
        campaign.save()

@shared_task
def schedule_sms_campaign(campaign_id, scheduled_time_str):
    from datetime import datetime
    scheduled_time = datetime.fromisoformat(scheduled_time_str)
    
    if timezone.now() >= scheduled_time:
        send_bulk_sms.delay(campaign_id)
    else:
        # Reschedule for later
        schedule_sms_campaign.apply_async(
            args=[campaign_id, scheduled_time_str],
            eta=scheduled_time
        )



