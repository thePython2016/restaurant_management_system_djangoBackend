from django.db import models
from django.contrib.auth.models import User

class SMSMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    from_phone = models.CharField(max_length=20)
    to_phone = models.CharField(max_length=20)
    message_body = models.TextField()
    message_sid = models.CharField(max_length=50, unique=True)
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-received_at']
        verbose_name = "SMS Message"
        verbose_name_plural = "SMS Messages"

    def __str__(self):
        return f"SMS from {self.from_phone}: {self.message_body[:50]}..."