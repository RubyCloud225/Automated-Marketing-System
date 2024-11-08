from flask import Flask, jsonify, request
from sqlalchemy import Boolean, create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# SQLAlchemy setup for SQL server
DATABASE_URL = 'mysql+pymysql://username:password@localhost/db_name'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define Url model for URL's table
class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=False)
    processed = Column(Boolean, default=False)

# Define Article Model
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

# Define Newsletter Model
class Newsletter(Base):
    __tablename__ = 'newsletters'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    status = Column(String(20), default='pending')

    def __repr__(self):
        return f"<Newsletter(id=self.id), status='{self.status}'>"

# Create tables
Base.metadata.create_all(engine)