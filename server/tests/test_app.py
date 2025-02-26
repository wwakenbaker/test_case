import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_deposit(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test/operation",
        params={"amount": 100, "operationType": "deposit"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 10100,
        "wallet_uuid": "test",
    }


@pytest.mark.anyio
async def test_deposit(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test/operation",
        params={"amount": 100, "operationType": "deposit"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 10100,
        "wallet_uuid": "test",
    }


@pytest.mark.anyio
async def test_deposit2(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test2/operation",
        params={"amount": 100, "operationType": "deposit"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 5100,
        "wallet_uuid": "test2",
    }


@pytest.mark.anyio
async def test_deposit_invalid_amount(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test2/operation",
        params={"amount": -100, "operationType": "deposit"},
    )
    assert response.status_code == 422
    assert response.json() == {"error": "Invalid amount"}


@pytest.mark.anyio
async def test_deposit_wallet_not_found(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test3/operation",
        params={"amount": 100, "operationType": "deposit"},
    )
    assert response.status_code == 404
    assert response.json() == {"error": "Wallet not found"}


@pytest.mark.anyio
async def test_withdraw(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test/operation",
        params={"amount": 200, "operationType": "withdraw"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 9900,
        "wallet_uuid": "test",
    }


@pytest.mark.anyio
async def test_withdraw2(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test2/operation",
        params={"amount": 200, "operationType": "withdraw"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 4900,
        "wallet_uuid": "test2",
    }


@pytest.mark.anyio
async def test_withdraw_insufficient(client: AsyncClient):
    response = await client.post(
        "/api/v1/wallets/test2/operation",
        params={"amount": 10000, "operationType": "withdraw"},
    )
    assert response.status_code == 422
    assert response.json() == {"error": "Insufficient funds"}


@pytest.mark.anyio
async def test_check_balance(client: AsyncClient):
    response = await client.get("/api/v1/wallets/test")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 9900,
        "wallet_uuid": "test",
    }


@pytest.mark.anyio
async def test_check_balance2(client: AsyncClient):
    response = await client.get("/api/v1/wallets/test2")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Successful.",
        "balance": 4900,
        "wallet_uuid": "test2",
    }


@pytest.mark.anyio
async def test_check_balance_not_found(client: AsyncClient):
    response = await client.get("/api/v1/wallets/test3")
    assert response.status_code == 404
    assert response.json() == {"error": "Wallet not found"}
