from django.contrib import admin
from .models import SMSMessage

@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ['from_phone', 'to_phone', 'message_body_preview', 'received_at', 'is_read']
    list_filter = ['is_read', 'received_at']
    search_fields = ['from_phone', 'to_phone', 'message_body']
    readonly_fields = ['message_sid', 'received_at']
    
    def message_body_preview(self, obj):
        return obj.message_body[:50] + "..." if len(obj.message_body) > 50 else obj.message_body
    message_body_preview.short_description = "Message Preview"