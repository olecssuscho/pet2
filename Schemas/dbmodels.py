from sqlalchemy import Column,String,Boolean,Float,Integer,Enum,ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    email = Column(String)
    password = Column(String)
    full_name  = Column(String)
    balance  = Column(Float)
    is_blocked  = Column(Boolean,default="False")
    created_at = Column(String)

class Transaction(Base):

    __tablename__ = "Transaction"

    id = Column(Integer,primary_key=True,autoincrement=True)
    sender_id = Column(Integer,ForeignKey(User.id))
    reciever_id = Column(Integer,ForeignKey(User.id))
    amount = Column(Float)
    status = Column(String,Enum("pending","success","failed","frozen",name = "status"),default="pending")
    type = Column(String,Enum("transfer","deposit","refund",name = "type"))

class PaymentRequest(Base):

    __tablename__ = "PaymentRequest"

    id = Column(Integer, primary_key=True,autoincrement=True)
    from_user_id = Column(Integer,ForeignKey(User.id))
    to_user_id = Column(Integer,ForeignKey(User.id))
    amount = Column(Float)
    message = Column(String)
    status = Column(String,Enum("pending","success","failed","frozen",name = "status"),default="pending")

class Refund(Base):

    __tablename__ = "Refund"

    id = Column(Integer, primary_key=True,autoincrement=True)    
    transaction_id = Column(Integer,ForeignKey(Transaction.id))
    reason = Column(String)
    status = Column(String,Enum("pending","success","failed","frozen",name = "status"),default="pending")