from fastapi import APIRouter

from .exchange import router as exchange_router

router = APIRouter(prefix="/api_v1")
router.include_router(exchange_router)
