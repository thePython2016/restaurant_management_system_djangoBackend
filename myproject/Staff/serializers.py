# Staff/serializers.py
from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['phone', 'firstName', 'lastName', 'position', 'email', 'address', 'region', 'salary']
    
    def validate_phone(self, value):
        if not value.startswith('+255'):
            raise serializers.ValidationError("Phone number must start with +255")
        return value
    
    def validate_salary(self, value):
        try:
            salary_int = int(value)
            if salary_int < 100000:
                raise serializers.ValidationError("Minimum salary is 100,000 TSh")
        except ValueError:
            raise serializers.ValidationError("Salary must be a valid number")
        return value