from sqlalchemy import Enum,ForeignKey,DateTime,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import timezone,datetime,timedelta
from sqlalchemy import JSON

class Base(DeclarativeBase):
    pass

class UserDB(Base):

    __tablename__ = "Users"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    role : Mapped[str] = mapped_column(default="user", nullable= True)
    email : Mapped[str] 
    password : Mapped[str] 
    full_name  : Mapped[str] 
    balance  : Mapped[float] 
    is_blocked  : Mapped[bool] = mapped_column(default=False) 
    refresh_token : Mapped[str] = mapped_column(nullable=True) 
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc)) 

class TransactionDB(Base):

    __tablename__ = "Transactions"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    asker : Mapped[str] = mapped_column(nullable=True) 
    sender_id : Mapped[int] = mapped_column(ForeignKey("Users.id"),nullable=True)
    attempted_sender_id : Mapped[int] = mapped_column(nullable=True)
    reciever_id : Mapped[int] = mapped_column(nullable=True)
    attempted_reciever_id : Mapped[int] = mapped_column(nullable=True)
    amount : Mapped[float] 
    attempted_sender_email : Mapped[str] = mapped_column(nullable=True)
    attempted_reciever_email : Mapped[str] = mapped_column(nullable=True)
    status : Mapped[str] = mapped_column(Enum("pending","success","failed","frozen",name = "status"), default="pending") 
    type : Mapped[str] = mapped_column(Enum("transfer","deposit","refund",name = "type"), default="transfer")  
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc)) 
    deleted_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class PaymentRequestDB(Base):

    __tablename__ = "PaymentRequests"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    asker : Mapped[str] = mapped_column(nullable=True) 
    from_user_id : Mapped[int] = mapped_column(ForeignKey("Users.id"))
    from_user_email : Mapped[str] 
    to_user_id : Mapped[int] = mapped_column(ForeignKey("Users.id"))
    to_user_email : Mapped[str]
    amount : Mapped[float] 
    message : Mapped[str] 
    status : Mapped[str] = mapped_column(Enum("pending","success","failed","frozen",name = "status"), default="pending") 
    type : Mapped[str] = mapped_column(Enum("transfer","deposit","refund",name = "type"), default="transfer", nullable=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("Transactions.id"), nullable=True)

class RefundDB(Base):

    __tablename__ = "Refunds"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)  
    asker : Mapped[str] = mapped_column(nullable=True) 
    transaction_id : Mapped[int] = mapped_column(ForeignKey("Transactions.id"))
    reason : Mapped[str] 
    status : Mapped[str] = mapped_column(Enum("pending","success","failed","frozen",name = "status"), default="pending") 

class WebhookDB(Base):

    __tablename__ = "Webhooks"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    url : Mapped[str] = mapped_column(nullable=True)
    email : Mapped[str] = mapped_column(nullable=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("Users.id"))

class WebhookLogDB(Base):

    __tablename__ = "WebhooksLog"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    webhook_id : Mapped[int] = mapped_column(ForeignKey("Webhooks.id"))
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    responce_status : Mapped[str]
    attempt_number : Mapped[int] = mapped_column(nullable=True)

class EmailLogDB(Base):

    __tablename__ = "EmailLogDB"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    webhook_id : Mapped[int] = mapped_column(ForeignKey("Webhooks.id"))
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    responce_status : Mapped[str]
    attempt_number : Mapped[int] = mapped_column(nullable=True)

class IdempotencyKeyDB(Base):

    __tablename__ = "IdempotencyKeyDB"
    __table_args__ = (UniqueConstraint("key", "user_id"),)

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    key : Mapped[str]
    user_id : Mapped[int] = mapped_column(ForeignKey("Users.id"))
    responce : Mapped[int] = mapped_column(JSON)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))
    expires_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc)+ timedelta(hours=24))
    transaction_id : Mapped[int] = mapped_column(ForeignKey("Transactions.id"))

class BlacklistDB(Base):

    __tablename__ = "Blacklist"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    ip : Mapped[str]
    reason : Mapped[str]
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AuditLogDB(Base):

    __tablename__ = "AuditLog"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("Users.id"))
    old_balance : Mapped[int]
    new_balance : Mapped[int]
    changed_by : Mapped[str]
    reason : Mapped[str]
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
