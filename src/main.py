from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.coins.aggregator import CoinAggregator
from src.exchanges.manager import ExchangeManager
from src.exchanges.router import router as exchanges_router
from src.router_page import router as pages_router
from src.spreads.calculator import SpreadCalculator
from src.spreads.router import router as spreads_router
from src.spreads.storage import SpreadStorage


@asynccontextmanager
async def lifespan(app: FastAPI):
    # components
    spread_storage = SpreadStorage()
    coin_aggregator = CoinAggregator()

    spread_calculator = SpreadCalculator(
        spread_storage=spread_storage,
        coin_aggregator=coin_aggregator,
    )

    exchange_manager = ExchangeManager(
        coin_aggregator=coin_aggregator,
    )

    # app state
    app.state.spread_storage = spread_storage
    app.state.coin_aggregator = coin_aggregator
    app.state.spread_calculator = spread_calculator
    app.state.exchange_manager = exchange_manager

    print("Инициализация приложения")

    exchange_manager.start()

    print(f"Приложение запущено. Бирж в работе: {len(exchange_manager.exchanges)}")

    try:
        yield
    finally:
        print("Остановка приложения")
        await exchange_manager.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(exchanges_router)
app.include_router(spreads_router)
app.include_router(pages_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
