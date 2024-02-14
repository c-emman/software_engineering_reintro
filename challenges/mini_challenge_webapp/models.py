from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_attributes: Mapped[str] = mapped_column(String)


class VATRates(Base):
    __tablename__ = 'vatrates'
    category: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)


class ProductsPydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    category: str
    type: Optional[str] = None
    price: Optional[float] = None
    quantity: int
    extra_attributes: Optional[str] = None


class VATRatesPydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: str
    rate: float

