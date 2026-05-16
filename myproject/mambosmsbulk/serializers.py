from rest_framework import serializers
from .models import SMSCampaign, SMSLog

class SMSCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCampaign
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'sent_at', 'status', 
                          'total_recipients', 'successful_sends', 'failed_sends')

class SMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSLog
        fields = '__all__'
