from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import select

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import Wallet
from schemas import WalletSchema

# Создание приложения
app = FastAPI()

#Создание движка и коннекта
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres_container:5432/postgres"
engine = create_async_engine(DATABASE_URL, echo=True)


# Запуск движка и создание сессии
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Создание тестовых кошельков
async def add_test_wallets():
    async with async_session() as session:
        async with session.begin():
            session.add(Wallet(id=1, wallet_uuid="test", balance=10000))
            session.add(Wallet(id=2, wallet_uuid="test2", balance=5000))
        return await session.commit()

#Заглушка
@app.get("/")
async def main():
    return "main"

#Проверка баланса по uuid
@app.get("/api/v1/wallets/{WALLET_UUID}", response_model=WalletSchema, status_code=200)
async def get_wallet(WALLET_UUID: str):
    async with async_session() as session:
        balance = await session.execute(
            select(Wallet.balance).where(Wallet.wallet_uuid == WALLET_UUID)
        )
        balance = balance.scalars().first()
        if balance is None:
            return JSONResponse({"error": "Wallet not found"}, status_code=404)
        return JSONResponse(
            {
            "message": "Successful.",
            "balance": balance,
            "wallet_uuid": WALLET_UUID
        }
        )

#Пополнение-вывод с кошелька по uuid
@app.post("/api/v1/wallets/{WALLET_UUID}/operation", status_code=200)
async def operation(WALLET_UUID: str, amount: int, operationType: str):
    async with async_session() as session:
        wallet = await session.execute(
            select(Wallet).where(Wallet.wallet_uuid == WALLET_UUID)
        )
        wallet = wallet.scalars().first()
        if wallet is None:
            return JSONResponse({"error": "Wallet not found"}, status_code=404)
        elif amount <= 0:
            return JSONResponse({"error": "Invalid amount"}, status_code=422)
        elif operationType.lower() == "deposit":
            wallet.balance += amount
        elif operationType.lower() == "withdraw":
            if wallet.balance < amount:
                return JSONResponse({"error": "Insufficient funds"}, status_code=422)
            wallet.balance -= amount
        else:
            return JSONResponse({"error": "Invalid operation type"}, status_code=422)

        await session.commit()
        return {
            "message": "Successful.",
            "balance": wallet.balance,
            "wallet_uuid": wallet.wallet_uuid,
        }


if __name__ == "__main__":
    import asyncio
    import uvicorn
    asyncio.run(add_test_wallets())
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
