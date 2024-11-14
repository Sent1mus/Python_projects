from pydantic import BaseModel, constr, field_validator

class Wallet(BaseModel):
    uuid: str  # Changed from constr to str
    balance: float
    version: int = 1  # Keep default value

class WalletOperation(BaseModel):
    amount: float

    @field_validator('amount')
    def check_amount(cls, v):
        if v == 0:  # Проверка на нулевую сумму
            raise ValueError('Amount must be non-zero')
        return v
