from fastapi import APIRouter

from src.exchanges.manager import get_names

router = APIRouter(prefix="/exchanges", tags=["Exchanges"])


@router.get('/')
async def get_exchanges():
    return get_names()
