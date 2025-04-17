
import os, time, subprocess, json, re
from pathlib import Path
from fastapi.responses import StreamingResponse, JSONResponse
from utils.utils import clean_url

downloads_dir = "./downloads"
Path(downloads_dir).mkdir(exist_ok=True)

async def download_video_stream(payload):
    try:
        url, formatId, isAudioOnly = payload.url, payload.formatId, payload.isAudioOnly
        if not url or not formatId:
            return JSONResponse(status_code=400, content={"error": "URL and format ID are required"})
        url = clean_url(url)
        print("Downloading video:", url)

        title_proc = subprocess.Popen(
            ["yt-dlp", "--get-title", "--restrict-filenames", url],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        title, title_err = title_proc.communicate()

        if title_proc.returncode != 0:
            return JSONResponse(status_code=500, content={"error": f"Failed to get video title: {title_err}"})

        sanitized_title = (
            title.strip().replace("/", "").replace("\\", "").replace(":", "")
                .replace("*", "").replace("?", "").replace("\"", "")
                .replace("<", "").replace(">", "").replace("|", "").replace(" ", "_")[:100]
        )

        print("Processing download for:", sanitized_title)

        timestamp = int(time.time())
        unique_id = f"{formatId}-{timestamp}"
        output_template = os.path.join(downloads_dir, f"{sanitized_title}-{unique_id}.%(ext)s")

        args = ["--no-playlist", "-o", output_template, "--newline"]
        if isAudioOnly:
            args += ["-f", formatId]
        else:
            if "tiktok.com" in url:
                args += ["--socket-timeout", "60", "--no-check-certificates", "-f", formatId]
            else:
                args += ["-f", f"{formatId}+bestaudio[ext=m4a]/bestaudio", "--merge-output-format", "mp4"]

        args.append(url)
        print("Running yt-dlp with args:", args)

        proc = subprocess.Popen(
            ["yt-dlp"] + args,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        def event_stream():
            for line in iter(proc.stdout.readline, ''):
                print("yt-dlp output:", line.strip())
                match = re.search(r"\\[download\\]\\s+(\\d+\\.\\d+)%\\s+of\\s+([\\d.]+\\w+)\\s+at\\s+([\\d.]+\\w+/s)\\s+ETA\\s+(\\d+:\\d+)", line)
                if match:
                    percent, totalSize, speed, eta = match.groups()
                    progress_data = {
                        "status": "downloading",
                        "percent": float(percent),
                        "totalSize": totalSize,
                        "speed": speed,
                        "eta": eta
                    }
                    yield f"data: {json.dumps(progress_data)}\\n\\n"
            proc.wait()

            if proc.returncode == 0:
                filename = next((f for f in os.listdir(downloads_dir) if f.startswith(f"{sanitized_title}-{unique_id}")), None)
                if filename:
                    print("Download completed:", filename)
                    yield f"data: {json.dumps({'status': 'completed', 'filename': filename, 'downloadPath': f'/downloads/{filename}'})}\\n\\n"
                else:
                    print("Could not find downloaded file")
                    yield f"data: {json.dumps({'status': 'error', 'message': 'File not found after download'})}\\n\\n"
            else:
                yield f"data: {json.dumps({'status': 'error', 'message': 'Download failed'})}\\n\\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        print("Error downloading video:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
