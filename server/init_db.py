import asyncio
from pyliquibase import Pyliquibase

#Запускается при поднятии docker compose,
#Инициализирует бд с помощью liquibase
async def init_db():
    liquibase = Pyliquibase(
            defaultsFile="liquibase_migrations/liquibase.properties"
    )
    liquibase.update()

if __name__ == "__main__":
    asyncio.run(init_db())