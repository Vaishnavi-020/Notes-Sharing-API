from .base import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password_hash=Column(String,nullable=False)

    notes=relationship("Note",back_populates="owner",cascade="all,delete-orphan")
