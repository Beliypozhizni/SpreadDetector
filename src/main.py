import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.coins.aggregator import CoinAggregator
from src.exchanges.manager import ExchangeManager
from src.spreads.calculator import SpreadCalculator

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("💰 Инициализация крипто-бирж...")

    coin_aggregator = CoinAggregator()
    exchange_manager = ExchangeManager(coin_aggregator)
    spread_calculator = SpreadCalculator(coin_aggregator)

    await exchange_manager.run()

    print(f"✅ Загружено бирж: {len(exchange_manager.exchanges)}")

    yield  # Приложение работает

    print("🛑 Остановка бирж...")
    exchange_manager.stop()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
