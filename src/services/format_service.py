import subprocess, time, json
from fastapi.responses import JSONResponse
from utils.utils import clean_url

async def fetch_formats(url: str):
    try:
        if not url:
            return JSONResponse(status_code=400, content={"error": "URL is required"})
        url = clean_url(url)
        print("Fetching formats for:", url)
        start_time = time.time()

        proc = subprocess.Popen(
            ["yt-dlp", "--dump-json", "--no-playlist", "--no-call-home", "--no-cache-dir", url],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        out, err = proc.communicate()
        print("yt-dlp stderr:", err)
        duration = time.time() - start_time
        print(f"yt-dlp-fetch took {duration:.2f} seconds")

        if proc.returncode != 0:
            return JSONResponse(status_code=500, content={"error": "Failed to fetch formats"})

        info = json.loads(out)
        return JSONResponse(content={"info": info})

    except Exception as e:
        print("Error fetching formats:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
