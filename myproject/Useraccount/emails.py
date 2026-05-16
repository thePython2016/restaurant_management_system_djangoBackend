from djoser.email import PasswordResetEmail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class CustomPasswordResetEmail(PasswordResetEmail):
    def send(self, to, *args, **kwargs):
        # Custom email content without templates
        user = self.context.get('user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        subject = "Reset Your ReactLife Password 🔐"
        
        # Plain text content
        text_content = f"""
Hello {user.first_name or user.username},

You requested a password reset for your ReactLife account.

Click this link to reset your password:
http://localhost:5173/password/reset/confirm?uid={uid}&token={token}

IMPORTANT:
• This link expires in 24 hours
• If you didn't request this, ignore this email
• Your current password remains unchanged until you create a new one

Need help? Contact our support team.

Best regards,
The ReactLife Team 🚀
        """
        
        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Password Reset</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">🚀 ReactLife</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9f9f9;">
                <h2 style="color: #333; margin-bottom: 20px;">Password Reset Request</h2>
                
                <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                
                <p>We received a request to reset your password for your ReactLife account. If you made this request, click the button below to create a new password:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5173/password/reset/confirm?uid={uid}&token={token}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 25px; 
                              display: inline-block;
                              font-weight: bold;
                              box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                        🔐 Reset My Password
                    </a>
                </div>
                
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #856404;"><strong>⚠️ Important Security Information:</strong></p>
                    <ul style="color: #856404; margin: 10px 0;">
                        <li>This link will expire in <strong>24 hours</strong></li>
                        <li>If you didn't request this reset, please ignore this email</li>
                        <li>Your current password will remain unchanged until you create a new one</li>
                    </ul>
                </div>
                
                <div style="background-color: #e8f4fd; border: 1px solid #b8daff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #004085;"><strong>💡 Having trouble?</strong></p>
                    <p style="color: #004085; margin: 5px 0;">If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #0066cc; font-size: 12px;">
                        http://localhost:5173/password/reset/confirm?uid={uid}&token={token}
                    </p>
                </div>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #666; font-size: 14px;">
                    Best regarrrrds,<br>
                    <strong>The ReactLife Team</strong> 🚀
                </p>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        This email wassss sent to {user.email}. If you have any questions, please contact our support team.
                    </p>
                </div>
            </div>
            
        </body>
        </html>
        """
        
        # Send email
        msg = EmailMultiAlternatives(subject, text_content, self.from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()