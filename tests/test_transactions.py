import pytest
from fastapi.testclient import TestClient
import threading
from main import app
from services.Transactions import transaction_service


user = TestClient(app)

def test_transactions():
    
    results = []
    
    user1 = user.post("/register", json={"email":"user1000",
                                         "password":"user10",
                                         "full_name":"user1",
                                         "balance":100})
    user1_email = user1.json()["email"]
    
    user2 = user.post("/register", json={"email":"user2000",
                                         "password":"user20",
                                         "full_name":"user2",
                                         "balance":0})
    user2_email = user2.json()["email"]

    def make_tr():
        transaction = user.post("/transaction", json={"sender_email":user1_email,
                                                      "reciever_email":user2_email,
                                                      "amount":20,
                                                      "status":"pending",
                                                      "type":"transfer"})

        results.append(transaction.status_code)
    
    transactions_10 = [threading.Thread(target=make_tr()) for _ in range(10)]

    for t in transactions_10:
        t.start()
    for t in transactions_10:
        t.join()

    assert 200 in results
    assert 422 in results


    