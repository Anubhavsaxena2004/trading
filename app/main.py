from fastapi import FastAPI, Depends
from .database import engine
from . import models
from .routers import trades
import os,math

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(trades.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Trading API running"}