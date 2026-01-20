from fastapi import APIRouter, Request

from src.dependencies.exchange_names import get_exchange_names

router = APIRouter(prefix="/exchanges", tags=["Exchanges"])


@router.get('/')
async def get_exchanges(request: Request):
    return get_exchange_names(request)
