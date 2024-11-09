from sqlalchemy import create_engine, sessionmaker
from models import Member

class LoginManager:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def login(self, email, password):
        session = self.Session()
        try:
            #Query the member by email
            member = session.query(Member).filter(Member.email == email).first()
            if member and member.check_password(password):
                print(f"Login successfuly for: {member.name}")
                return True #Login successful
            else:
                print(f"Login failed for: {email}")
                return False #Login failed
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            session.close()
    

