import psycopg2
from datetime import datetime
import random
import sys
import uuid  # Импортируем библиотеку uuid

def generate_random_uuid():
    return str(uuid.uuid4())  # Генерируем корректный UUID

def generate_random_float(min_value=-1000, max_value=1000):
    return round(random.uniform(min_value, max_value), 2)

def generate_fake_wallet():
    uuid = generate_random_uuid()
    balance = generate_random_float(-1000, 1000)
    version = 1
    created_at = datetime.now().isoformat()
    updated_at = created_at

    return {
        "uuid": uuid,
        "balance": balance,
        "version": version,
        "created_at": created_at,
        "updated_at": updated_at
    }

def generate_fake_operation(existing_wallets):
    wallet_uuid = random.choice(existing_wallets)
    amount = generate_random_float(-1000, 1000)
    timestamp = datetime.now().isoformat()

    return {
        "wallet_uuid": wallet_uuid,
        "amount": amount,
        "timestamp": timestamp
    }

def main():
    print("Starting data generation...")

    # Database connection settings
    db_settings = {
        "dbname": "wallet_management",
        "user": "postgres",
        "password": "944577",
        "host": "localhost",
        "port": "5432"
    }

    try:
        conn = psycopg2.connect(**db_settings)
        print("Подключение к БД успешно.")
        cur = conn.cursor()

        # Set UTF-8 encoding explicitly
        cur.execute("SET client_encoding TO 'UTF8';")

        # Проверка соединения
        cur.execute("SELECT 1;")
        print("Соединение проверено.")

        # Generate fake wallets
        print("Generating fake wallets...")
        existing_wallets = []  # Список для хранения UUID созданных кошельков
        for _ in range(10):
            wallet_data = generate_fake_wallet()
            insert_query = """
                INSERT INTO wallets (uuid, balance, version, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            try:
                cur.execute(insert_query, (
                    wallet_data["uuid"],
                    wallet_data["balance"],
                    wallet_data["version"],
                    wallet_data["created_at"],
                    wallet_data["updated_at"]
                ))
                existing_wallets.append(wallet_data["uuid"])  # Добавляем UUID в список
            except Exception as e:
                print(f"Error inserting wallet data: {e}")
                print(f"Problematic data: {wallet_data}")
                sys.exit(1)

        # Generate fake operations
        print("Generating fake operations...")
        for _ in range(10):
            operation_data = generate_fake_operation(existing_wallets)  # Передаем существующие кошельки
            insert_query = """
                INSERT INTO operations (wallet_uuid, amount, timestamp)
                VALUES (%s, %s, %s)
            """
            try:
                cur.execute(insert_query, (
                    operation_data["wallet_uuid"],
                    operation_data["amount"],
                    operation_data["timestamp"]
                ))
            except Exception as e:
                print(f"Error inserting operation data: {e}")
                print(f"Problematic data: {operation_data}")
                sys.exit(1)

        conn.commit()

        # Print wallet contents
        print("Wallet contents:")
        cur.execute("SELECT * FROM wallets")
        wallets = cur.fetchall()
        for wallet in wallets:
            print(wallet)

        # Print operation contents
        print("\nOperation contents:")
        cur.execute("SELECT * FROM operations")
        operations = cur.fetchall()
        for operation in operations:
            print(operation)

        cur.close()
        conn.close()
        print("Connection closed successfully.")

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()