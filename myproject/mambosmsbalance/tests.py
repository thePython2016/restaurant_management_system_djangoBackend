from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

class SMSBalanceViewsTest(APITestCase):
    """Test cases for SMS balance views"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_sms_balance_requires_authentication(self):
        """Test that SMS balance endpoint requires authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('mambosmsbalance:sms-balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch('requests.get')
    def test_get_sms_balance_success(self, mock_get):
        """Test successful SMS balance retrieval"""
        # Mock successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'balance': 150.50,
            'currency': 'TZS'
        }
        mock_get.return_value.raise_for_status.return_value = None
        
        url = reverse('mambosmsbalance:sms-balance')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['balance'], 150.50)
        self.assertEqual(response.data['currency'], 'TZS')
    
    @patch('requests.get')
    def test_get_sms_balance_api_error(self, mock_get):
        """Test handling of API errors"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        url = reverse('mambosmsbalance:sms-balance')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response.data['success'])
        self.assertIn('error', response.data)
