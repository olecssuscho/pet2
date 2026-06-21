from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import pytest
from schemas.dbmodels import UserDB, TransactionDB, PaymentRequestDB, RefundDB
from sqlalchemy.orm import sessionmaker
from main import app
from dependency import get_db
from schemas.dbmodels import Base

TEST_DATABASE_URL = "postgresql://postgres:123qwe@localhost:5432/postgres_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def clear_db():
    db = TestingSession()
    db.query(RefundDB).delete()
    db.query(TransactionDB).delete()
    db.query(PaymentRequestDB).delete()
    db.query(UserDB).delete()
    db.commit()
    db.close()
    yield


client = TestClient(app)