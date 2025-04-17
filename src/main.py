from fastapi import FastAPI
import os
import sys
from dotenv import load_dotenv
from api import routes_root, routes_fetch_formats, routes_download

load_dotenv()

endpoint = os.getenv("APPWRITE_FUNCTION_API_ENDPOINT")
project_id = os.getenv("APPWRITE_FUNCTION_PROJECT_ID")
api_key = os.getenv("APPWRITE_FUNCTION_API_KEY")

app = FastAPI()

# Include all your routers
app.include_router(routes_root.router)
app.include_router(routes_download.router)
app.include_router(routes_fetch_formats.router)

# This is needed for Appwrite custom function runtime
async def main(context):
    # Appwrite just expects this to exist
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "✅ FastAPI Appwrite Function Executed"
    }

# This is for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
