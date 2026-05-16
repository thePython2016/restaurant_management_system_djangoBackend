# Mambo SMS Balance App

This Django app provides SMS balance checking functionality with full authentication context and request tracking.

## Features

- **Authentication Required**: All endpoints require user authentication
- **Request Tracking**: Every balance request is logged with user context
- **IP Address Logging**: Client IP addresses are recorded for security
- **User Agent Tracking**: Browser/client information is captured
- **Comprehensive History**: Users can view their balance request history
- **Statistics**: Detailed statistics about balance requests
- **Error Handling**: Proper error handling and logging

## API Endpoints

### 1. Get SMS Balance
- **URL**: `/api/sms/balance/`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Retrieves current SMS balance from Mambo SMS service
- **Response**: JSON with balance, currency, and request details

### 2. Get Balance History
- **URL**: `/api/sms/balance/history/`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Returns user's balance request history
- **Response**: JSON with list of previous requests and statistics

### 3. Get Balance Statistics
- **URL**: `/api/sms/balance/statistics/`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Provides comprehensive statistics about user's balance requests
- **Response**: JSON with success rates, total requests, and recent balance

## Authentication

All endpoints require a valid authentication token. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Models

### SMSBalanceRequest
- `user`: Foreign key to User model
- `request_timestamp`: When the request was made
- `response_status`: Success/error status
- `response_data`: JSON response from SMS service
- `error_message`: Error details if request failed
- `ip_address`: Client IP address
- `user_agent`: Client browser/application info

## Usage Examples

### Check Balance
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/sms/balance/
```

### Get History
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/sms/balance/history/
```

### Get Statistics
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/sms/balance/statistics/
```

## Security Features

- **Authentication Required**: All endpoints are protected
- **IP Logging**: Tracks client IP addresses for security monitoring
- **User Context**: Every request is tied to a specific user
- **Read-only Admin**: Admin interface prevents manual manipulation
- **Request Validation**: Proper input validation and sanitization

## Dependencies

- Django REST Framework
- Django authentication system
- Requests library for HTTP calls
- JSON field support

## Configuration

Ensure the following settings are configured in your Django settings:

```python
MAMBO_SMS_API_KEY = 'your_api_key'
MAMBO_SMS_BASE_URL = 'https://api.mambo.co.tz'
```

## Testing

Run the test suite:

```bash
python manage.py test mambosmsbalance
```

## Admin Interface

The admin interface provides:
- View all balance requests
- Filter by status, user, and date
- Search functionality
- Read-only access for security
