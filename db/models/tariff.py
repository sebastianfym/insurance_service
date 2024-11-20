import decimal
from sqlalchemy import String, DateTime, Integer, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from db.database import Base


class Tariff(Base):
    __tablename__ = "tariff"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, unique=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    cargo_type: Mapped[String] = mapped_column(String(100), unique=False, index=True, nullable=False)
    rate: Mapped[decimal.Decimal] = mapped_column(Float, nullable=False)
