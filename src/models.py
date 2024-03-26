from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # POSTGRESQL_USERNAME: str
    # POSTGRESQL_PASSWORD: str
    # POSTGRESQL_PORT: int
    # POSTGRESQL_HOST: str
    # POSTGRESQL_DATABASE: str
    #
    # SQLITE_DATABASE: str
    POSTGRESQL_USERNAME: str = "default_user"
    POSTGRESQL_PASSWORD: str = "default_pass"
    POSTGRESQL_PORT: int = 5432
    POSTGRESQL_HOST: str = "localhost"
    POSTGRESQL_DATABASE: str = "test_db"
    SQLITE_DATABASE: str = "sqlite:///test.db"
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()


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
