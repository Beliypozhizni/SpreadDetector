import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.exchanges.router import router as exchanges_router
from src.spreads.router import router as spreads_router
from src.router_page import router as pages_router
from src.coins.aggregator import CoinAggregator
from src.exchanges.manager import ExchangeManager
from src.spreads.calculator import SpreadCalculator
from src.spreads.storage import SpreadStorage


async def create_components():
    spread_storage = SpreadStorage()
    coin_aggregator = CoinAggregator()

    spread_calculator = SpreadCalculator(
        spread_storage=spread_storage,
        coin_aggregator=coin_aggregator,
    )
    exchange_manager = ExchangeManager(
        coin_aggregator=coin_aggregator,
    )

    return {
        spread_storage.__class__.__name__: spread_storage,
        coin_aggregator.__class__.__name__: coin_aggregator,
        spread_calculator.__class__.__name__: spread_calculator,
        exchange_manager.__class__.__name__: exchange_manager,
    }


async def cleanup_components(components: dict):
    cleanup_tasks = []

    if ExchangeManager.__name__ in components:
        cleanup_tasks.append(components[ExchangeManager.__name__].stop())

    await asyncio.gather(*cleanup_tasks, return_exceptions=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    components = await create_components()
    exchange_manager = components[ExchangeManager.__name__]

    print("Инициализация приложения")

    asyncio.create_task(exchange_manager.run())

    print(f"Приложение запущено. Бирж в работе: {len(exchange_manager.exchanges)}")

    yield components

    print("Остановка приложения")
    await cleanup_components(components)


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
