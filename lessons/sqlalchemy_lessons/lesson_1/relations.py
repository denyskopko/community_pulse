# Типы связей таблиц
from sqlalchemy import (
    create_engine,
    BigInteger,
    ForeignKey,
    String,
    SmallInteger,
    Boolean
)

from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from pathlib import Path


BASE_DIR = Path(__file__).parents[2]


# engine = create_engine(
#     url=f"sqlite:///{BASE_DIR / 'relations.db'}"
# )

engine = create_engine(
    url="sqlite:///:memory:"
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        unique=True
    )



class UsersCourses(Base):
    __tablename__ = 'users_courses'

    course_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('courses.id')
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id')
    )


# One to Many
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

    # FK keys
    address_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('addresses.id')
    )

    # relationships
    address = relationship(
        'Address',
        back_populates='users'
    )

    profile = relationship(
        'UserProfile',
        back_populates='user',
        uselist=False
    )

    courses = relationship(
        'Course',
        secondary='UsersCourses',
        back_populates='users'
    )


class Course(Base):
    __tablename__ = "courses"

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    users = relationship(
        'User',
        secondary='UsersCourses',
        back_populates='courses'
    )



# One to One
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    avatar: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    # FK keys
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        unique=True
    )

    # relationships
    user = relationship(
        'User',
        back_populates='profile',
        uselist=False
    )


class Address(Base):
    __tablename__ = "addresses"

    city: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    # relationships
    users = relationship(
        'User',
        back_populates='address'
    )

    # example
    # <field_name> = relationship(
    #     '<class Name>',
    #     back_populates='<class Name> -> <field name>'
    # )


# user = User()
#
# user.address
#
# address = Address()
# address.users