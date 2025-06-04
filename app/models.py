from sqlalchemy import Column, String, Float, Integer, DateTime
from .database import Base

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    side = Column(String, nullable=False)  # "buy" or "sell"
    timestamp = Column(DateTime, nullable=False)

class AveragePrice(Base):
    __tablename__ = "avg_prices"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    avg_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)