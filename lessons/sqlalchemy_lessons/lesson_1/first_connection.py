from sqlalchemy import (
    create_engine,
    BigInteger,
    Column,
    String,
    SmallInteger,
    Boolean
)

from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column
)
from pathlib import Path


BASE_DIR = Path(__file__).parents[2]
print(__file__)
print(BASE_DIR)

engine = create_engine(
    url=f"sqlite:///{BASE_DIR / 'database.db'}"
)


class Base(DeclarativeBase):
    __abstract__ = True

    # python type = int

    # DB type:  SmallInteger | Integer | BigInteger

    # python type = str

    # DB type:  String | Text

    # v1
    # id = Column(
    #     BigInteger,
    #     primary_key=True,
    #     autoincrement=True,
    #     unique=True
    # )

    # v2
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        unique=True
    )


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(
        String(25),     # VARCHAR(25)
        nullable=False  # NOT NULL
    )
    surname: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )
    username: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        unique=True,
        index=True
    )
    age: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,  # сторона ORM и python
        server_default='true', # сторона базы данных
    )


user = User()

Base.metadata.create_all(bind=engine)

print("ALL TABLES WAS CREATED")
print(Base.metadata.tables)


# Session = sessionmaker(
#     bind=engine,
# )
#
#
#
# session = Session()


# user = User(**data)  # transient
#
# session.add(user)  # pending
#
# session.flush() \ session.commit()  # persistent
#
#
# user: User = select(User).where(User.id = id_) # detached
# session.close()
#
# session.delete(user)  # deleted
# session.commit()
