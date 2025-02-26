from pydantic import BaseModel


class WalletSchema(BaseModel):
    wallet_uuid: str
    balance: int
