import time


VIEWER_TIMEOUT = 15

viewers = {}


def heartbeat(stream_id: str, viewer_id: str):
    if stream_id not in viewers:
        viewers[stream_id] = {}

    viewers[stream_id][viewer_id] = time.time()

    return True


def get_viewer_count(stream_id: str):
    if stream_id not in viewers:
        return 0

    now = time.time()

    active_viewers = {
        viewer_id: last_seen
        for viewer_id, last_seen in viewers[stream_id].items()
        if now - last_seen <= VIEWER_TIMEOUT
    }

    viewers[stream_id] = active_viewers

    return len(active_viewers)


def remove_viewer(stream_id: str, viewer_id: str):
    if stream_id in viewers:
        viewers[stream_id].pop(viewer_id, None)


def clear_stream_viewers(stream_id: str):
    viewers.pop(stream_id, None)
