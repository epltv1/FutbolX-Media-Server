from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from server.streams import (
    create_stream,
    get_streams,
    get_stream,
    delete_stream
)

from server.ffmpeg import (
    start_ffmpeg,
    stop_ffmpeg,
    is_running
)

from server.viewers import (
    heartbeat,
    get_viewer_count,
    remove_viewer
)


app = FastAPI(
    title="FutbolX Media Server",
    version="1.0.0"
)


# -----------------------------
# REQUEST MODELS
# -----------------------------

class StreamCreate(BaseModel):
    name: str
    source: str


class ViewerHeartbeat(BaseModel):
    viewer_id: str


# -----------------------------
# BASIC
# -----------------------------

@app.get("/")
def root():
    return {
        "name": "FutbolX Media Server",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------
# STREAMS
# -----------------------------

@app.get("/api/streams")
def list_streams():
    result = []

    for stream in get_streams():
        stream_copy = stream.copy()

        stream_copy["running"] = is_running(
            stream["id"]
        )

        stream_copy["viewers"] = get_viewer_count(
            stream["id"]
        )

        result.append(stream_copy)

    return {
        "streams": result
    }


@app.post("/api/streams")
def add_stream(data: StreamCreate):

    stream = create_stream(
        data.name,
        data.source
    )

    try:
        start_ffmpeg(
            stream["id"],
            stream["source"]
        )

        stream["status"] = "live"

    except Exception as error:

        delete_stream(stream["id"])

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    return stream


@app.post("/api/streams/{stream_id}/stop")
def stop_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    stopped = stop_ffmpeg(stream_id)

    if stopped:
        stream["status"] = "offline"

    return {
        "success": stopped,
        "stream": stream
    }


@app.post("/api/streams/{stream_id}/restart")
def restart_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    stop_ffmpeg(stream_id)

    start_ffmpeg(
        stream_id,
        stream["source"]
    )

    stream["status"] = "live"

    return stream


@app.delete("/api/streams/{stream_id}")
def remove_stream(stream_id: str):

    stream = get_stream(stream_id)

    if not stream:
        raise HTTPException(
            status_code=404,
            detail="Stream not found"
        )

    stop_ffmpeg(stream_id)

    delete_stream(stream_id)

    return {
        "success": True,
        "message": "Stream deleted"
    }


# -----------------------------
# VIEWERS
# -----------------------------

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

    heartbeat(
        stream_id,
        data.viewer_id
    )

    return {
        "viewers": get_viewer_count(stream_id)
    }


@app.delete("/api/streams/{stream_id}/viewer/{viewer_id}")
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
