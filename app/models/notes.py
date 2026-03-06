from .base import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,DateTime,Text
from sqlalchemy.orm import relationship
from sqlalchemy import func

class Note(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True)
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    subject=Column(String,nullable=False)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    is_private=Column(Boolean,nullable=False)
    file_path=Column(String,nullable=False)
    content=Column(Text,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    owner=relationship("User",back_populates="notes")

