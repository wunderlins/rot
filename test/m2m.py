#!/usr/bin/env python

import os, sys, re
sys.path.append(os.path.join('..', 'lib', 'SQLAlchemy', 'lib'))
sys.path.append(os.path.join('..'))

import config

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# relational features
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

dsn = "sqlite:///../data/m2m.db"
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine(dsn, echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship("Address", backref='user',
                    cascade="all, delete, delete-orphan")

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password'%s')>" % (
                               self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    
    """
    def __init__(self, keyword):
        self.keyword = keyword
    """

class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword', secondary=post_keywords, backref='posts')
    
    """
    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body
    """
    
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)  # once engine is available
session = Session()

def create_user(session):
	simon = User(name="Simon", fullname="Simon Wunderlin", password='1234')
	simon.addresses = [
		Address(email_address='swunderlin@gmail.com'), 
		Address(email_address='simon.wunderlin@usb.ch')
	]
	session.add(simon)
	session.commit()


