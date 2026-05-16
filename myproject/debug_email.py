import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_connection():
    try:
        print("🔍 Testing SMTP connection with detailed debugging...")
        
        # Test basic socket connection first
        print("1. Testing socket connection to smtp.gmail.com:587...")
        sock = socket.create_connection(('smtp.gmail.com', 587), timeout=10)
        sock.close()
        print("✅ Socket connection successful")
        
        # Test SMTP connection
        print("2. Creating SMTP connection...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.set_debuglevel(2)  # Maximum debug output
        
        print("3. Starting TLS...")
        server.starttls()
        
        print("4. Attempting login...")
        server.login('piliomari20th@gmail.com', 'kgzkhtlmlsqtbpai')
        
        print("5. Creating test message...")
        msg = MIMEMultipart()
        msg['From'] = 'piliomari20th@gmail.com'
        msg['To'] = 'piliomari20th@gmail.com'
        msg['Subject'] = 'SMTP Test'
        
        body = "This is a test email from Django troubleshooting"
        msg.attach(MIMEText(body, 'plain'))
        
        print("6. Sending email...")
        text = msg.as_string()
        server.sendmail('piliomari20th@gmail.com', 'piliomari20th@gmail.com', text)
        
        print("7. Closing connection...")
        server.quit()
        
        print("✅ SUCCESS: All tests passed!")
        return True
        
    except socket.timeout:
        print("❌ ERROR: Connection timed out")
        print("💡 Check your internet connection or firewall settings")
        return False
    except socket.gaierror as e:
        print(f"❌ ERROR: DNS resolution failed: {e}")
        print("💡 Check your internet connection")
        return False
    except ConnectionResetError:
        print("❌ ERROR: Connection reset by peer")
        print("💡 Gmail might be rate limiting or blocking your IP temporarily")
        return False
    except smtplib.SMTPServerDisconnected:
        print("❌ ERROR: Server unexpectedly disconnected")
        print("💡 Try again in a few minutes, or try SSL (port 465)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    test_smtp_connection()