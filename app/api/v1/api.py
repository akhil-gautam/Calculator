from fastapi import APIRouter

from app.api.v1.endpoints import users, login, campaigns, bids, social_media_stats

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(bids.router, prefix="/bids", tags=["bids"])
api_router.include_router(
    social_media_stats.router, prefix="/social-media-stats", tags=["social-media-stats"]
)