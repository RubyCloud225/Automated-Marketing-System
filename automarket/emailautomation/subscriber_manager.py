from models import EmailSubscribers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SubscriberManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_subscriber(self, email, first_name=None, last_name=None):
        """Add a new subscriber."""
        new_subscriber = EmailSubscribers(email=email, first_name=first_name, last_name=last_name)
        self.session.add(new_subscriber)
        self.session.commit()
        print(f"Subscriber {email} added successfully")
    
    def delete_subscriber(self, subscriber_id):
        """Delete Subscriber"""
        subscriber = self.session.query(EmailSubscribers).filter_by(id=subscriber_id).first()
        if subscriber:
            self.session.delete(subscriber)
            self.session.commit()
            print(f"Subscriber {subscriber_id} deleted successfully")
        else:
            print(f"Subscriber with ID {subscriber_id} not found")
    
    def get_subscribers(self):
        """Retrieve all active subscribers"""
        subscribers = self.session.query(EmailSubscribers).filter_by(is_active=True).all()
        return [{'id': sub.id, 'email': sub.email, 'first_name': sub.first_name, 'last_name': sub.last_name} for sub in subscribers]
    
    def save(self):
        """Save the current session."""
        self.session.commit()

    def close(self):
        """Close the session."""
        self.session.close()