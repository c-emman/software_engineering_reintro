from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String, nullable=False)
    Category: Mapped[str] = mapped_column(String, nullable=False)
    Type: Mapped[str] = mapped_column(String)
    Price: Mapped[float] = mapped_column(Float)
    Quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    Extra_attributes: Mapped[str] = mapped_column(String)


class VATRates(Base):
    __tablename__ = 'vat_rates'
    Category: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
