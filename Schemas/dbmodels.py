from sqlalchemy import Column,String,Boolean,Float,Integer,Enum,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base
from datetime import timezone,datetime

Base = declarative_base()

class UserDB(Base):

    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    email = Column(String)
    password = Column(String)
    full_name  = Column(String)
    balance  = Column(Float)
    is_blocked  = Column(Boolean,default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransactionDB(Base):

    __tablename__ = "Transaction"

    id = Column(Integer,primary_key=True,autoincrement=True)
    sender_id = Column(Integer,ForeignKey(UserDB.id),nullable=True)
    attempted_sender_id = Column(Integer, nullable=True)
    reciever_id = Column(Integer,ForeignKey(UserDB.id),nullable=True)
    attempted_reciever_id = Column(Integer, nullable=True)
    amount = Column(Float)
    attempted_sender_email = Column(String, nullable=True)
    attempted_reciever_email = Column(String, nullable=True)
    status = Column(String,Enum("pending","success","failed","frozen",name = "status"),default="pending")
    type = Column(String,Enum("transfer","deposit","refund",name = "type"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PaymentRequestDB(Base):

    __tablename__ = "PaymentRequest"

    id = Column(Integer, primary_key=True,autoincrement=True)
    from_user_id = Column(Integer,ForeignKey(UserDB.id))
    to_user_id = Column(Integer,ForeignKey(UserDB.id))
    amount = Column(Float)
    message = Column(String)
    status = Column(String,Enum("pending","success","failed","frozen",name = "status"),default="pending")

class RefundDB(Base):

    __tablename__ = "Refund"

    id = Column(Integer, primary_key=True,autoincrement=True)    
    transaction_id = Column(Integer,ForeignKey(TransactionDB.id))
    reason = Column(String)
    status = Column(String,Enum("pending","success","failed","frozen",name = "status"),default="pending")