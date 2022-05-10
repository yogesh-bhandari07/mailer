import datetime
from http import client
from database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text, DateTime

class Mailer(Base):
    __tablename__='mailer'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False)
    client_id=Column(String(255),nullable=False)
    created_on=Column(DateTime,default=datetime.datetime.now())


class Clients(Base):
    __tablename__='client'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(255),nullable=False)
    created_on=Column(DateTime,default=datetime.datetime.now())
    


   

