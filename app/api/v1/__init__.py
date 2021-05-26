from fastapi import APIRouter

from . import category

api_router = APIRouter()
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
