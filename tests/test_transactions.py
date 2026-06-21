import pytest
from fastapi.testclient import TestClient
import threading
from main import app
from conftest import client


def test_transactions():
    user1 = client.post("/user/login", data={"username": "user1000", "password": "user10"})
    
    if user1.status_code == 404:
        client.post("/register", json={"email": "user1000", "password": "user10", "full_name": "user1", "balance": 100})
        client.post("/register", json={"email": "user2000", "password": "user20", "full_name": "user2", "balance": 0})

    results = []

    def make_tr():
        with TestClient(app) as client:
            token = client.post("/user/login", data={"username": "user1000", "password": "user10"}).json()["access_token"]
            transaction = client.post("/transaction",
                json={"reciever_email": "user2000", "amount": 20, "type": "transfer"},
                headers={"Authorization": f"Bearer {token}"}
            )
            results.append(transaction.status_code)

    transactions_10 = [threading.Thread(target=make_tr) for _ in range(10)]
    for t in transactions_10:
        t.start()
    for t in transactions_10:
        t.join()

    assert 200 in results
    assert 422 in results


    