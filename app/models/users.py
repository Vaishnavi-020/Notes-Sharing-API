from .base import Base
from sqlalchemy import Column,Integer,String

class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password_hash=Column(String,nullable=False)
