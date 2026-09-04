import os
import shutil
import signal
import subprocess


HLS_ROOT = "/var/www/futbolx/hls"

processes = {}


def get_output_dir(stream_id: str):
    return os.path.join(HLS_ROOT, stream_id)


def get_output_file(stream_id: str):
    return os.path.join(
        get_output_dir(stream_id),
        "index.m3u8"
    )


def start_ffmpeg(stream_id: str, source: str):
    if not source or not source.strip():
        raise ValueError("A source URL is required to start the stream")

    # If an old process exists, stop it first.
    if is_running(stream_id):
        stop_ffmpeg(stream_id)

    output_dir = get_output_dir(stream_id)

    # Remove old HLS files before starting.
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    os.makedirs(output_dir, exist_ok=True)

    output_file = get_output_file(stream_id)

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",

        "-i", source.strip(),

        "-c", "copy",

        "-f", "hls",

        "-hls_time", "4",
        "-hls_list_size", "6",

        "-hls_flags",
        "delete_segments+append_list",

        output_file
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    processes[stream_id] = process

    return {
        "stream_id": stream_id,
        "pid": process.pid,
        "output": output_file
    }


def stop_ffmpeg(stream_id: str):
    process = processes.get(stream_id)
    stopped = False

    if process:
        try:
            if process.poll() is None:
                # Kill the complete FFmpeg process group.
                try:
                    os.killpg(
                        os.getpgid(process.pid),
                        signal.SIGTERM
                    )
                except ProcessLookupError:
                    pass

                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(
                            os.getpgid(process.pid),
                            signal.SIGKILL
                        )
                    except ProcessLookupError:
                        pass

                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        pass

            stopped = True

        except Exception:
            try:
                process.kill()
            except Exception:
                pass

            stopped = True

        finally:
            processes.pop(stream_id, None)

    # Always delete the HLS directory.
    # This makes the M3U8 and TS files immediately disappear.
    output_dir = get_output_dir(stream_id)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

        if not os.path.exists(output_dir):
            stopped = True

    return stopped


def is_running(stream_id: str):
    process = processes.get(stream_id)

    if not process:
        return False

    running = process.poll() is None

    if not running:
        processes.pop(stream_id, None)

    return running


def get_process(stream_id: str):
    return processes.get(stream_id)
