import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
SMTP_SERVER = ""
SMTP_PORT = 587
SENDER_EMAIL = ""  
SENDER_PASSWORD = ""  
RECIPIENT_EMAIL = ""  

def send():
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Automated Email - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = """
        Hello!
        
        This is an automated email sent from your Python scheduler.
        
        Best regards,
        Your Automation Bot
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        
        # Login
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        
        # Close session
        server.quit()
        
        print(f"[{datetime.now()}] Email sent successfully!")
        
    except Exception as e:
        print(f"[{datetime.now()}] Failed to send email: {str(e)}")

if __name__ == "__main__":
    # Test the email function
    send() 