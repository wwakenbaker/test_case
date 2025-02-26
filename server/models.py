from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

#Модель кошелька
class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_uuid: Mapped[int] = mapped_column(String(length=36), unique=True)
    balance: Mapped[int] = mapped_column(Integer)
