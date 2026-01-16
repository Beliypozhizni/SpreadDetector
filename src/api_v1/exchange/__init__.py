from fastapi import APIRouter

from .views import router as exchange_router

router = APIRouter(prefix="/exchanges", tags=["Exchange"])
router.include_router(exchange_router)
