
from fastapi import APIRouter
from models.video_models import DownloadVideoRequest
from services.download_service import download_video_stream

router = APIRouter()

@router.post("/api/download-video")
async def download_video(payload: DownloadVideoRequest):
    return await download_video_stream(payload)
