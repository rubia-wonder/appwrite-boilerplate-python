from fastapi import FastAPI
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api import routes_root, routes_fetch_formats, routes_download


# Load .env vars if available
load_dotenv()

endpoint = os.getenv("APPWRITE_FUNCTION_API_ENDPOINT")
project_id = os.getenv("APPWRITE_FUNCTION_PROJECT_ID")
api_key = os.getenv("APPWRITE_FUNCTION_API_KEY")

app = FastAPI()

# Include all your routers
app.include_router(routes_root.router)
app.include_router(routes_download.router)
app.include_router(routes_fetch_formats.router)
