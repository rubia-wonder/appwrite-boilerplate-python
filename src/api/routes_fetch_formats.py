
from fastapi import APIRouter
from models.video_models import FetchFormatsRequest
from services.format_service import fetch_formats

router = APIRouter()

@router.post("/api/fetch-formats")
async def fetch_formats_route(payload: FetchFormatsRequest):
    return await fetch_formats(payload.url)
