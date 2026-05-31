import subprocess
import os

def extract_audio(video_path, output_audio="temp/audio.wav"):
    os.makedirs("temp", exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 🔥 DEBUG CHECK (important)
    if not os.path.exists(output_audio):
        print("❌ FFmpeg ERROR OUTPUT:")
        print(result.stderr)
        raise FileNotFoundError("Audio file was NOT created")

    return output_audio