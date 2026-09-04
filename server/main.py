import time

import psutil

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from server.streams import (
    create_stream,
    get_streams,
    get_stream,
    delete_stream,
    update_stream_source,
    mark_stream_live,
    mark_stream_stopped
)

from server.ffmpeg import (
    start_ffmpeg,
    stop_ffmpeg,
    is_running
)

from server.viewers import (
    heartbeat,
    get_viewer_count,
    remove_viewer,
    clear_stream_viewers
)


app = FastAPI(
    title="FutbolX Media Server",
    version="1.1.0"
)


# --------------------------------
# DASHBOARD
# --------------------------------

app.mount(
    "/dashboard",
    StaticFiles(directory="dashboard", html=True),
    name="dashboard"
)


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("dashboard/index.html")


# --------------------------------
# REQUEST MODELS
# --------------------------------

class StreamCreate(BaseModel):
    name: str
    source: str = ""


class StreamSourceUpdate(BaseModel):
    source: str


class ViewerHeartbeat(BaseModel):
    viewer_id: str


# --------------------------------
# BASIC
# --------------------------------

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "server": "online",
        "version": "1.1.0"
    }


@app.get("/api/health/stats")
def health_stats():
    streams = get_streams()

    active_streams = 0
    total_viewers = 0

    for stream in streams:
        running = is_running(stream["id"])

        if running:
            active_streams += 1

        total_viewers += get_viewer_count(
            stream["id"]
        )

    # VPS statistics
    cpu = psutil.cpu_percent(interval=None)

    memory = psutil.virtual_memory()

    uptime_seconds = int(
        time.time() - psutil.boot_time()
    )

    return {
        "status": "online",
        "active_streams": active_streams,
        "total_streams": len(streams),
        "total_viewers": total_viewers,

        "cpu": {
            "percent": cpu
        },

        "memory": {
            "percent": memory.percent,
            "used": memory.used,
            "total": memory.total
        },

        "uptime_seconds": uptime_seconds
    }


# --------------------------------
# STREAMS
# --------------------------------

@app.get("/api/streams")
def list_streams():
    result = []

    for stream in get_streams():

        stream_copy = stream.copy()

        running = is_running(
            stream["id"]
        )

        stream_copy["running"] = running

        stream_copy["viewers"] = get_viewer_count(
            stream["id"]
        )

        if running:
            stream_copy["status"] = "live"

        elif stream_copy.get("source"):
            if stream_copy["status"] == "live":
                stream_copy["status"] = "ready"

        else:
            stream_copy["status"] = "scheduled"

        # Never expose internal filesystem paths.
        stream_copy["m3u8"] = (
            f"/hls/{stream['id']}/index.m3u8"
            if running
            else None
        )

        result.append(stream_copy)

    return {
        "streams": result
    }


# --------------------------------
# CREATE STREAM
# --------------------------------

@app.post("/api/streams")
def add_stream(data: StreamCreate):

    if not data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Stream name is required"
        )

    stream = create_stream(
        data.name,
        data.source
    )

    return stream


# --------------------------------
# ADD / UPDATE SOURCE
# --------------------------------

@app.put("/api/streams/{stream_id}/source")
def add_source(
    stream_id: str,
    data: StreamSourceUpdate
):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    if not data.source.strip():
        raise HTTPException(
            status_code=400,
            detail="Source URL is required"
        )

    updated = update_stream_source(
        stream_id,
        data.source
    )

    return updated


# --------------------------------
# START STREAM
# --------------------------------

@app.post("/api/streams/{stream_id}/start")
def start_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    if not stream.get("source"):
        raise HTTPException(
            status_code=400,
            detail="Add a source URL before starting this stream"
        )

    if is_running(stream_id):
        return {
            "success": True,
            "message": "Stream is already running",
            "stream": stream
        }

    try:

        start_ffmpeg(
            stream_id,
            stream["source"]
        )

        mark_stream_live(
            stream_id
        )

    except Exception as error:

        stop_ffmpeg(stream_id)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    return {
        "success": True,
        "stream": stream
    }


# --------------------------------
# STOP STREAM
# --------------------------------

@app.post("/api/streams/{stream_id}/stop")
def stop_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    # Kill FFmpeg + delete HLS files.
    stop_ffmpeg(stream_id)

    # Remove all viewers associated with the stream.
    clear_stream_viewers(stream_id)

    # Remove stream from the live/stream list completely.
    delete_stream(stream_id)

    return {
        "success": True,
        "message": "Stream stopped and removed"
    }


# --------------------------------
# RESTART STREAM
# --------------------------------

@app.post("/api/streams/{stream_id}/restart")
def restart_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    if not stream.get("source"):
        raise HTTPException(
            status_code=400,
            detail="Add a source URL before restarting"
        )

    stop_ffmpeg(stream_id)

    clear_stream_viewers(stream_id)

    try:

        start_ffmpeg(
            stream_id,
            stream["source"]
        )

        mark_stream_live(
            stream_id
        )

    except Exception as error:

        stop_ffmpeg(stream_id)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    return {
        "success": True,
        "stream": stream
    }


# --------------------------------
# DELETE STREAM
# --------------------------------

@app.delete("/api/streams/{stream_id}")
def remove_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    stop_ffmpeg(stream_id)

    clear_stream_viewers(stream_id)

    delete_stream(stream_id)

    return {
        "success": True,
        "message": "Stream deleted"
    }


# --------------------------------
# VIEWERS
# --------------------------------

@app.post("/api/streams/{stream_id}/viewer")
def viewer_heartbeat(
    stream_id: str,
    data: ViewerHeartbeat
):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    if not is_running(stream_id):
        raise HTTPException(
            status_code=404,
            detail="Stream is not live"
        )

    heartbeat(
        stream_id,
        data.viewer_id
    )

    return {
        "viewers": get_viewer_count(
            stream_id
        )
    }


@app.delete(
    "/api/streams/{stream_id}/viewer/{viewer_id}"
)
def viewer_leave(
    stream_id: str,
    viewer_id: str
):

    remove_viewer(
        stream_id,
        viewer_id
    )

    return {
        "success": True
            }
