import os
import subprocess


HLS_ROOT = "/var/www/futbolx/hls"

processes = {}


def start_ffmpeg(stream_id: str, source: str):
    output_dir = os.path.join(HLS_ROOT, stream_id)

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "index.m3u8")

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",

        "-i", source,

        "-c", "copy",

        "-f", "hls",
        "-hls_time", "4",
        "-hls_list_size", "6",
        "-hls_flags", "delete_segments+append_list",

        output_file
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )

    processes[stream_id] = process

    return {
        "stream_id": stream_id,
        "pid": process.pid,
        "output": output_file
    }


def stop_ffmpeg(stream_id: str):
    process = processes.get(stream_id)

    if not process:
        return False

    process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

    del processes[stream_id]

    return True


def is_running(stream_id: str):
    process = processes.get(stream_id)

    if not process:
        return False

    return process.poll() is None


def get_process(stream_id: str):
    return processes.get(stream_id)
