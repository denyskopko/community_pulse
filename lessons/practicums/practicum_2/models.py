from sqlalchemy import Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )


class Mineral(Base):
    __tablename__ = "minerals"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    color: Mapped[str] = mapped_column(String(30))
    hardness: Mapped[float] = mapped_column(Float)

    # # Связи
    # shipments: Mapped[list["Shipment"]] = relationship(back_populates="mineral")
    # prices: Mapped[list["Price"]] = relationship(back_populates="mineral")
    #

class Salon(Base):
    __tablename__ = "salons"
    __table_args__ = (  # эта настройка помогает задать дополнительные конфигурации таблицы
        UniqueConstraint("name", "location"),  # а тут мы говорим: сочетание названия салона и его адреса должно быть уникальным
    )

    name: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(100))

    # # Связи
    # employees: Mapped[list["Employee"]] = relationship(back_populates="salon")
    # shipments_details: Mapped[list["SalonShipmentAssociation"]] = relationship(
    #     back_populates="salon",
    #     cascade="all, delete-orphan",
    # )
    # shipments = association_proxy("shipments_details", "shipment")
    #
