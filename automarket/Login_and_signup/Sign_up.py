from sqlalchemy import create_engine, sessionmaker
from automarket.data.models import Member


class MemberManager:
    def __init__(self, connection_string):
        #Create a new SQLAlchemy engine
        self.engine = create_engine(connection_string)
        #Create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)
    
    def add_member(self, name, email, password):
        #Create a new session
        session = self.Session()
        try:
            #Create a new member instance
            new_member = Member(name=name, email=email)
            new_member.set_password(password) #Hash the password
            #Add the new member to the session
            session.add(new_member)
            #Commit the session to save the changes
            session.commit()
            print(f"Added member: {new_member}")
        except Exception as e:
            # Roll back the session in case of an error
            session.rollback()
            print(f"Error adding member: {e}")
        finally:
            #Close the session
            session.close()
    
    def get_member(self, email):
        session = self.Session()
        try:
            return session.query(Member).filter_by(email=email).first()
        finally:
            session.close()
    
    def update_member(self, email, name=None, password=None):
        session = self.Session()
        try:
            member = session.query(Member).filter_by(email=email).first()
            if member:
                if name:
                    member.name = name
                if password:
                    member.set_password(password)
                session.commit()
                return member
            return None
        except Exception as e:
            session.rollback()
            print(f"Error updating member: {e}")
            return None
        finally: session.close()
    
    def delete_member(self, email):
        session = self.Session()
        try:
            member = session.query(Member).filter_by(email=email).first()
            if member:
                session.delete(member)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting member: {e}")
            return False
        finally:
            session.close()
