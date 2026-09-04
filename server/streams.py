import uuid
from datetime import datetime


streams = {}


def create_stream(name: str, source: str):
    stream_id = str(uuid.uuid4())[:8]

    stream = {
        "id": stream_id,
        "name": name,
        "source": source,
        "status": "offline",
        "viewers": 0,
        "created_at": datetime.utcnow().isoformat()
    }

    streams[stream_id] = stream

    return stream


def get_streams():
    return list(streams.values())


def get_stream(stream_id: str):
    return streams.get(stream_id)


def delete_stream(stream_id: str):
    if stream_id in streams:
        del streams[stream_id]
        return True

    return False
