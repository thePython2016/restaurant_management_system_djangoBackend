import smtplib
from email.mime.text import MIMEText

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('piliomari20th@gmail.com', 'kgzkhtlmlsqtbpai')
    
    msg = MIMEText('Test message')
    msg['Subject'] = 'Test'
    msg['From'] = 'piliomari20th@gmail.com'
    msg['To'] = 'test@example.com'
    
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")