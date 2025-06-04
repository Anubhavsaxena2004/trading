from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Trade, AveragePrice
from ..schemas import TradeCreate, AvgPriceCreate

router = APIRouter()

@router.post("/trades")
def add_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = Trade(**trade.dict(), timestamp=datetime.now())
    db.add(db_trade)
    db.commit()
    return {"status": "Trade added"}

@router.get("/trades")
def get_trades(
    ticker: str = None, 
    start_date: datetime = None, 
    end_date: datetime = None, 
    db: Session = Depends(get_db)
):
    query = db.query(Trade)
    if ticker: 
        query = query.filter(Trade.ticker == ticker)
    if start_date:
        query = query.filter(Trade.timestamp >= start_date)
    if end_date:
        query = query.filter(Trade.timestamp <= end_date)
    return query.all()

@router.post("/avg-prices")
def add_avg_price(avg_price: AvgPriceCreate, db: Session = Depends(get_db)):
    db_avg_price = AveragePrice(**avg_price.dict())
    db.add(db_avg_price)
    db.commit()
    return {"status": "Average price recorded"}