from liquibase import LiquidBase
from sqlalchemy import create_engine

def main():
    # Подключение к базе данных
    db_url = "postgresql://postgres:944577@localhost/wallet_management"
    engine = create_engine(db_url)

    # Инициализация Liquibase
    liquidbase = LiquidBase(engine)

    # Применение изменений из changelog.xml
    liquidbase.update()

if __name__ == "__main__":
    main()