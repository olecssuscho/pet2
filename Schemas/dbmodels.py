from sqlalchemy import Column,String,Boolean,Float,Integer
from sqlalchemy.orm import declarative_base 

Base = declarative_base()

class User(Base):

    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    email = Column(String)
    password = Column(String)
    full_name  = Column(String)
    balance  = Column(Float)
    is_blocked  = Column(Boolean)
    created_at = Column(String)