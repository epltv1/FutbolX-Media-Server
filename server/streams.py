import uuid
from datetime import datetime, timezone


streams = {}


def create_stream(name: str, source: str = ""):
    stream_id = str(uuid.uuid4())[:8]

    stream = {
        "id": stream_id,
        "name": name.strip(),
        "source": source.strip(),
        "status": "scheduled" if not source.strip() else "ready",
        "viewers": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "started_at": None
    }

    streams[stream_id] = stream

    return stream


def get_streams():
    return list(streams.values())


def get_stream(stream_id: str):
    return streams.get(stream_id)


def update_stream_source(stream_id: str, source: str):
    stream = streams.get(stream_id)

    if not stream:
        return None

    stream["source"] = source.strip()

    if stream["status"] != "live":
        stream["status"] = "ready"

    return stream


def mark_stream_live(stream_id: str):
    stream = streams.get(stream_id)

    if not stream:
        return None

    stream["status"] = "live"
    stream["started_at"] = datetime.now(timezone.utc).isoformat()

    return stream


def mark_stream_stopped(stream_id: str):
    stream = streams.get(stream_id)

    if not stream:
        return None

    stream["status"] = "ready" if stream.get("source") else "scheduled"
    stream["started_at"] = None
    stream["viewers"] = 0

    return stream


def delete_stream(stream_id: str):
    if stream_id in streams:
        del streams[stream_id]
        return True

    return False
