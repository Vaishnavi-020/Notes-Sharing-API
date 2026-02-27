from .base import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Boolean

class Notes(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True)
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    subject=Column(String,nullable=False)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    is_private=Column(Boolean,nullable=False)
