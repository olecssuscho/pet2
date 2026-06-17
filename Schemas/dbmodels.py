from sqlalchemy import Enum,ForeignKey
from sqlalchemy.orm import declarative_base,DeclarativeBase,Mapped,mapped_column
from datetime import timezone,datetime

Base = declarative_base()

class UserDB(Base):

    __tablename__ = "Users"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    email : Mapped[str] 
    password : Mapped[str] 
    full_name  : Mapped[str] 
    balance  : Mapped[float] 
    is_blocked  : Mapped[bool] = mapped_column(default=False) 
    created_at : Mapped[datetime] = mapped_column(time_zone=True, default= lambda: datetime.now(timezone.utc)) 

class TransactionDB(Base):

    __tablename__ = "Transaction"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    sender_id : Mapped[int] = mapped_column(ForeignKey(UserDB.id),nullable=True)
    attempted_sender_id : Mapped[int] = mapped_column(nullable=True)
    reciever_id : Mapped[int] = mapped_column(nullable=True)
    attempted_reciever_id : Mapped[int] = mapped_column(nullable=True)
    amount : Mapped[float] 
    attempted_sender_email : Mapped[str] = mapped_column(nullable=True)
    attempted_reciever_email : Mapped[str] = mapped_column(nullable=True)
    status : Mapped[str] = mapped_column(Enum("pending","success","failed","frozen",name = "status"), default="pending") 
    type : Mapped[str] = mapped_column(Enum("transfer","deposit","refund",name = "type"), default="pending")  
    created_at : Mapped[datetime] = mapped_column(time_zone=True, default= lambda: datetime.now(timezone.utc)) 


class PaymentRequestDB(Base):

    __tablename__ = "PaymentRequest"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    from_user_id : Mapped[int] = mapped_column(ForeignKey(UserDB.id))
    to_user_id : Mapped[int] = mapped_column(ForeignKey(UserDB.id))
    amount : Mapped[float] 
    message : Mapped[str] 
    status : Mapped[str] = mapped_column(Enum("pending","success","failed","frozen",name = "status"), default="pending") 

class RefundDB(Base):

    __tablename__ = "Refund"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)  
    transaction_id : Mapped[int] = mapped_column(ForeignKey(TransactionDB.id))
    reason : Mapped[str] 
    status : Mapped[str] = mapped_column(Enum("pending","success","failed","frozen",name = "status"), default="pending") 