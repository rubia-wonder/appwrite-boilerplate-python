from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
import os
from dotenv import load_dotenv
import uvicorn
from api import routes_root, routes_fetch_formats, routes_download
from fastapi import FastAPI

# Load environment variables from .env file
load_dotenv()

# Access variables
endpoint = os.getenv("APPWRITE_FUNCTION_API_ENDPOINT")
project_id = os.getenv("APPWRITE_FUNCTION_PROJECT_ID")
api_key = os.getenv("APPWRITE_FUNCTION_API_KEY")

app = FastAPI()

app.include_router(routes_root.router)
app.include_router(routes_download.router)
app.include_router(routes_fetch_formats.router)


# This Appwrite function will be executed every time your function is triggered
# def main():
#     print(f'Entering into python functions ...')
#     # You can use the Appwrite SDK to interact with other services
#     # For this example, we're using the Users service
#     client = (
#         Client()
#         .set_endpoint(endpoint)
#         .set_project(project_id)
#         .set_key(api_key)
#     )
#     users = Users(client)
#     print('Users: ', users)

#     return (
#         {
#             "motto": "Build like a team of hundreds_",
#             "learn": "https://appwrite.io/docs",
#             "connect": "https://appwrite.io/discord",
#             "getInspired": "https://builtwith.appwrite.io",
#         }
#     )

# if __name__ == "__main__":
#     result = main()
#     print(result)

if __name__ == "__main__":
    # Start the FastAPI server using uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)