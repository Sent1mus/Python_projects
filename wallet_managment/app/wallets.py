from fastapi import APIRouter, HTTPException, Depends
from app.database import get_wallet, update_wallet_balance, log_operation, database, create_wallet_in_db
from app.schemas import WalletOperation, Wallet
import re

router = APIRouter()

@router.post("/")
async def create_wallet(wallet: Wallet):
    try:
        await create_wallet_in_db(wallet.uuid, wallet.balance)
        return {"balance": wallet.balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{wallet_uuid}")
async def get_balance(wallet_uuid: str):
    if not re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', wallet_uuid):
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    wallet = await get_wallet(wallet_uuid)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}

@router.post("/{wallet_uuid}/operation")
async def perform_operation(wallet_uuid: str, operation: WalletOperation):
    if not re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', wallet_uuid):
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    async with database.transaction():
        wallet = await get_wallet(wallet_uuid)
        if wallet is None:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if operation.amount < 0 and wallet.balance < abs(operation.amount):
            raise HTTPException(status_code=400, detail="Insufficient funds")

        current_version = wallet.version
        wallet = await get_wallet(wallet_uuid)  # Повторное получение кошелька для проверки версии
        if wallet.version != current_version:
            raise HTTPException(status_code=409, detail="Conflict: data has been modified")

        new_balance = wallet.balance + operation.amount
        await update_wallet_balance(wallet_uuid, new_balance, wallet.version + 1)
        await log_operation(wallet_uuid, operation.amount)

        return {"balance": new_balance}
