from pydantic import BaseModel

class FetchFormatsRequest(BaseModel):
    url: str

class DownloadVideoRequest(BaseModel):
    url: str
    formatId: str
    isAudioOnly: bool = False
