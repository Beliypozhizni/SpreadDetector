from fastapi import APIRouter

from src.exchanges import get_names

router = APIRouter()


@router.get('/')
async def get_exchanges():
    return get_names()
