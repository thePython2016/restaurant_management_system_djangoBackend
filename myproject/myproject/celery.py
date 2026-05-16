# your_project/celery.py (create this in your project root directory)
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# your_project/__init__.py (modify this file in your project root)
from .celery import app as celery_app

__all__ = ('celery_app',)


# sms_app/tasks.py (create this in your app directory)
from celery import shared_task
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings
from .models import SMSCampaign, SMSMessage, Contact
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@shared_task
def send_bulk_sms(campaign_id):
    """
    Send SMS messages for a bulk campaign
    """
    try:
        campaign = SMSCampaign.objects.get(id=campaign_id)
        
        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Get all unique recipients
        all_recipients = set()
        
        # Add individual contacts
        for contact in campaign.recipients.all():
            if contact.is_active:
                all_recipients.add(contact)
        
        # Add contacts from groups
        for group in campaign.recipient_groups.all():
            for contact in group.contacts.filter(is_active=True):
                all_recipients.add(contact)
        
        # Update total recipients count
        campaign.total_recipients = len(all_recipients)
        campaign.save()
        
        successful_sends = 0
        failed_sends = 0
        
        # Send SMS to each recipient
        for recipient in all_recipients:
            try:
                # Send SMS via Twilio
                message = client.messages.create(
                    body=campaign.message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=recipient.phone_number
                )
                
                # Create success record
                SMSMessage.objects.create(
                    campaign=campaign,
                    recipient=recipient,
                    message_sid=message.sid,
                    status='sent',
                    sent_at=timezone.now()
                )
                successful_sends += 1
                
                logger.info(f"SMS sent successfully to {recipient.phone_number}")
                
            except Exception as e:
                # Create failure record
                SMSMessage.objects.create(
                    campaign=campaign,
                    recipient=recipient,
                    status='failed',
                    error_message=str(e)
                )
                failed_sends += 1
                logger.error(f"Failed to send SMS to {recipient.phone_number}: {e}")
        
        # Update campaign with results
        campaign.successful_sends = successful_sends
        campaign.failed_sends = failed_sends
        campaign.status = 'completed'
        campaign.sent_at = timezone.now()
        campaign.save()
        
        logger.info(f"Campaign {campaign.name} completed: {successful_sends} sent, {failed_sends} failed")
        return f"Campaign completed: {successful_sends} sent, {failed_sends} failed"
        
    except SMSCampaign.DoesNotExist:
        logger.error(f"Campaign {campaign_id} not found")
        return f"Campaign {campaign_id} not found"
    except Exception as e:
        logger.error(f"Campaign {campaign_id} failed: {e}")
        try:
            campaign = SMSCampaign.objects.get(id=campaign_id)
            campaign.status = 'failed'
            campaign.save()
        except:
            pass
        return f"Campaign failed: {e}"


@shared_task
def schedule_sms_campaign(campaign_id, scheduled_time_str):
    """
    Schedule an SMS campaign for future sending
    """
    try:
        # Parse the scheduled time
        scheduled_time = datetime.fromisoformat(scheduled_time_str.replace('Z', '+00:00'))
        current_time = timezone.now()
        
        # If the scheduled time has passed, send immediately
        if current_time >= scheduled_time:
            logger.info(f"Scheduled time passed, sending campaign {campaign_id} immediately")
            return send_bulk_sms.delay(campaign_id)
        else:
            # Schedule the task to run at the specified time
            logger.info(f"Scheduling campaign {campaign_id} for {scheduled_time}")
            return send_bulk_sms.apply_async(
                args=[campaign_id],
                eta=scheduled_time
            )
            
    except Exception as e:
        logger.error(f"Error scheduling campaign {campaign_id}: {e}")
        try:
            campaign = SMSCampaign.objects.get(id=campaign_id)
            campaign.status = 'failed'
            campaign.save()
        except:
            pass
        return f"Scheduling failed: {e}"


@shared_task
def update_sms_status():
    """
    Periodic task to update SMS delivery status from Twilio
    This can be run as a periodic task to check delivery status
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Get messages that are still pending delivery confirmation
        pending_messages = SMSMessage.objects.filter(
            status='sent',
            message_sid__isnull=False
        )
        
        updated_count = 0
        for sms_message in pending_messages:
            try:
                # Fetch message status from Twilio
                message = client.messages(sms_message.message_sid).fetch()
                
                # Update status based on Twilio response
                if message.status in ['delivered', 'undelivered', 'failed']:
                    sms_message.status = 'delivered' if message.status == 'delivered' else 'failed'
                    if message.status in ['undelivered', 'failed']:
                        sms_message.error_message = f"Twilio status: {message.status}"
                    sms_message.save()
                    updated_count += 1
                    
            except Exception as e:
                logger.error(f"Error updating SMS status for message {sms_message.id}: {e}")
        
        logger.info(f"Updated status for {updated_count} SMS messages")
        return f"Updated {updated_count} messages"
        
    except Exception as e:
        logger.error(f"Error in update_sms_status task: {e}")
        return f"Status update failed: {e}"


@shared_task
def cleanup_old_campaigns():
    """
    Cleanup old completed campaigns (optional maintenance task)
    """
    from datetime import timedelta
    
    try:
        # Delete campaigns older than 90 days
        cutoff_date = timezone.now() - timedelta(days=90)
        old_campaigns = SMSCampaign.objects.filter(
            status='completed',
            created_at__lt=cutoff_date
        )
        
        count = old_campaigns.count()
        old_campaigns.delete()
        
        logger.info(f"Cleaned up {count} old campaigns")
        return f"Cleaned up {count} old campaigns"
        
    except Exception as e:
        logger.error(f"Error in cleanup task: {e}")
        return f"Cleanup failed: {e}"


# Management command to test tasks
# Create: sms_app/management/commands/test_sms.py
"""
from django.core.management.base import BaseCommand
from sms_app.tasks import send_bulk_sms
from sms_app.models import SMSCampaign

class Command(BaseCommand):
    help = 'Test SMS sending'

    def add_arguments(self, parser):
        parser.add_argument('campaign_id', type=str, help='Campaign ID to send')

    def handle(self, *args, **options):
        campaign_id = options['campaign_id']
        try:
            campaign = SMSCampaign.objects.get(id=campaign_id)
            self.stdout.write(f'Sending campaign: {campaign.name}')
            result = send_bulk_sms.delay(campaign_id)
            self.stdout.write(f'Task queued with ID: {result.id}')
        except SMSCampaign.DoesNotExist:
            self.stderr.write(f'Campaign {campaign_id} not found')
"""