import databases
import sqlalchemy
from typing import Union
from app.schemas import Wallet
from sqlalchemy.exc import IntegrityError
import logging
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db/wallet_management")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Определяем таблицу кошельков
wallets = sqlalchemy.Table(
    "wallets",
    metadata,
    sqlalchemy.Column("uuid", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("balance", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("version", sqlalchemy.Integer, nullable=False, default=1),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

# Определяем таблицу операций
operations = sqlalchemy.Table(
    "operations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("wallet_uuid", sqlalchemy.String(36)),
    sqlalchemy.Column("amount", sqlalchemy.Float),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

logger = logging.getLogger("wallet_management")
logging.basicConfig(level=logging.INFO)

async def get_wallet(uuid: str) -> Union[Wallet, None]:
    query = wallets.select().where(wallets.c.uuid == uuid)
    return await database.fetch_one(query)

async def update_wallet_balance(uuid: str, balance: float, version: int):
    query = wallets.update().where(wallets.c.uuid == uuid).values(
        balance=balance, version=version
    )
    await database.execute(query)
    logger.info(f"Updated wallet {uuid}: new balance = {balance}")

async def log_operation(wallet_uuid: str, amount: float):
    query = operations.insert().values(wallet_uuid=wallet_uuid, amount=amount)
    await database.execute(query)

async def create_wallet_in_db(uuid: str, balance: float):
    if balance < 0:
        raise ValueError("Initial balance cannot be negative.")

    query = wallets.insert().values(uuid=uuid, balance=balance, version=1)
    try:
        await database.execute(query)
    except IntegrityError:
        raise Exception("Wallet with this UUID already exists.")
