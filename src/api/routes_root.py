from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Video Downloader API is running 🚀"}
