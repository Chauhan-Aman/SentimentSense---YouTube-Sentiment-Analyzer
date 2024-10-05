from fastapi import APIRouter
from service.api.endpoints.yt_test import yt_router
from service.api.endpoints.comment_test import comment_router

main_router = APIRouter()

main_router.include_router(yt_router)
main_router.include_router(comment_router)