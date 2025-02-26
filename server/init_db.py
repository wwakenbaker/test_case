import asyncio
from pyliquibase import Pyliquibase

from app import engine, async_session
from models import Base, Wallet


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        liquibase = Pyliquibase(
            defaultsFile="liquibase_migrations/liquibase.properties"
        )
        liquibase.update()

    async with async_session() as session:
        async with session.begin():
            session.add(Wallet(id=1, wallet_uuid="test", balance=10000))
            session.add(Wallet(id=2, wallet_uuid="test2", balance=5000))
        return await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db())