from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

def test_deposit():
    response = client.post("/api/v1/wallets/test/operation", params={"amount": 100, "operationType": "deposit"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successful.", "balance": 10100, "wallet_uuid": "test"}

def test_deposit2():
    response = client.post("/api/v1/wallets/test2/operation", params={"amount": 100, "operationType": "deposit"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successful.", "balance": 5100, "wallet_uuid": "test2"}

def test_deposit_invalid_amount():
    response = client.post("/api/v1/wallets/test2/operation", params={"amount": -100, "operationType": "deposit"})
    assert response.status_code == 422
    assert response.json() == {"error": "Invalid amount"}

def test_deposit_wallet_not_found():
    response = client.post("/api/v1/wallets/test3/operation", params={"amount": 100, "operationType": "deposit"})
    assert response.status_code == 404
    assert response.json() == {"error": "Wallet not found"}

def test_withdraw():
    response = client.post("/api/v1/wallets/test/operation", params={"amount": 200, "operationType": "withdraw"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successful.", "balance": 9900, "wallet_uuid": "test"}

def test_withdraw2():
    response = client.post("/api/v1/wallets/test2/operation", params={"amount": 200, "operationType": "withdraw"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successful.", "balance": 4900, "wallet_uuid": "test2"}

def test_withdraw_insufficient():
    response = client.post("/api/v1/wallets/test2/operation", params={"amount": 10000, "operationType": "withdraw"})
    assert response.status_code == 422
    assert response.json() == {"error": "Insufficient funds"}

def test_check_balance():
    response = client.get("/api/v1/wallets/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Successful.", "balance": 9900, "wallet_uuid": "test"}

def test_check_balance2():
    response = client.get("/api/v1/wallets/test2")
    assert response.status_code == 200
    assert response.json() == {"message": "Successful.", "balance": 4900, "wallet_uuid": "test2"}

def test_check_balance_not_found():
    response = client.get("/api/v1/wallets/test3")
    assert response.status_code == 404
    assert response.json() == {"error": "Wallet not found"}
