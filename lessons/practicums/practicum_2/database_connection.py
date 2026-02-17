from pathlib import Path

from sqlalchemy import create_engine


BASE_DIR = Path(__file__).parent.parent

DATABASE_URL = f"sqlite:///{BASE_DIR}/minerals_system.db"


engine = create_engine(
    DATABASE_URL,
    echo=True,  # Показывать SQL запросы в консоли
    future=True  # Использовать SQLAlchemy 2.0 стиль
)
