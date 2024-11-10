import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from automarket.data.models import EmailSubscribers, Newsletter

Base = declarative_base()

class NewsletterEmailManager:
    def __init__(self, database_url, smtp_server, smtp_port, smtp_user, smtp_password):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
    
    def send_newsletter(self, newsletter_id):
        """Send the approved newsletter to all active subscribers"""
        session = self.Session()

        #Fetch the newsletter
        newsletter = self.session.query(Newsletter).filter_by(id=newsletter_id, is_approved=True).first()
        if not newsletter:
            print(f"Newsletter with ID {newsletter_id} is not approved or does not exist")
            return
        subscribers = self.session.query(EmailSubscribers).filter_by(is_active=True).all()
        for subscriber in subscribers:
            self._send_email(subscriber.email, newsletter.subject, newsletter.content)

        session.close()

    def _send_email(self, to_email, subject, content):
        """Send an email using SMTP"""
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(content, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                print(f"Newsletter sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
"""
# Example usage
if __name__ == "__main__":
    DATABASE_URI = 'sqlite:///subscribers.db'  # Use SQLite for simplicity
    SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
    SMTP_PORT = 587  # Common SMTP port for TLS
    SMTP_USER = 'your_email@example.com'  # Your email
    SMTP_PASSWORD = 'your_email_password'  # Your email password

    newsletter_manager = NewsletterManager(DATABASE_URI, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)

    # Example of sending a newsletter with ID 1
    newsletter_manager.send_newsletter(1)

"""