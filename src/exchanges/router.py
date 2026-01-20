from fastapi import APIRouter, Request, status

from src.dependencies.exchange_names import get_exchange_names

router = APIRouter(prefix="/exchanges", tags=["Exchanges"])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_exchanges(request: Request):
    return get_exchange_names(request)
