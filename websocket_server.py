import os
import json
import asyncio
import datetime
import websockets
import subprocess

RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

async def handle_connection(websocket):
    first_message = await websocket.recv()
    info = json.loads(first_message)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    tab_id = str(info.get("tabId", "tab"))

    filename_base = f"{tab_id}_{timestamp}"
    base_output_path = os.path.join(RECORDINGS_DIR, f"{filename_base}_%03d.wav")

    ffmpeg = subprocess.Popen([
        'ffmpeg',
        '-f', 'webm',
        '-i', 'pipe:0',
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        '-f', 'segment',
        '-segment_time', '5',
        base_output_path
    ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    print(f"record start: {base_output_path}")

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                ffmpeg.stdin.write(message)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        ffmpeg.stdin.close()
        ffmpeg.wait()

        print(f"record end: {RECORDINGS_DIR}")

async def main():
    print("websockets server start")

    async with websockets.serve(handle_connection, "0.0.0.0", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
