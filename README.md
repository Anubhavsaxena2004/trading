# Trading System

A comprehensive trading system with REST API, real-time data processing, and AWS integration.

## Features

- REST API for managing trades
- Real-time stock price monitoring via WebSockets
- Background task processing with Celery and Redis
- AWS Lambda integration for data analysis
- Moving Average Crossover trading strategy (optional)

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL
- Redis

### Local Development Setup

1. Clone the repository

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt