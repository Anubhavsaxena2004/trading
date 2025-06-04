from celery import Celery
from redis import Redis

celery = Celery(__name__, broker="redis://localhost:6379/0")

@celery.task
def notify_threshold(ticker, price):
    # Simulate notification (e.g., email/log)
    print(f"ALERT: {ticker} at ${price} crossed threshold")