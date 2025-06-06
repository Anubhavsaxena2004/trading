from pydantic import BaseModel, validator
from datetime import datetime
import os,math
class TradeCreate(BaseModel):
    ticker: str
    price: float
    quantity: int
    side: str

    @validator('price')
    def price_positive(cls, v):
        if v <= 0: raise ValueError("Price must be positive")
        return v

    @validator('side')
    def valid_side(cls, v):
        if v not in ["buy", "sell"]: 
            raise ValueError("Side must be 'buy' or 'sell'")
        return v


class AvgPriceCreate(BaseModel):
    ticker: str
    avg_price: float
    timestamp: datetime