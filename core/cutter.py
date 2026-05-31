import os
import subprocess
from moviepy import VideoFileClip, TextClip, CompositeVideoClip


# -----------------------------------------------------
# FAST CUT (UNCHANGED)
# -----------------------------------------------------
def cut_clip(video_path, start, end, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", video_path,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac",
        output_path
    ]

    subprocess.run(cmd, check=True)


# -----------------------------------------------------
# 🔥 WORD-BY-WORD TIKTOK CAPTIONS ENGINE
# -----------------------------------------------------
def burn_subtitles(video_path, srt_path, output_path):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    video = VideoFileClip(video_path)

    # -----------------------------
    # SIMPLE SRT PARSER
    # -----------------------------
    def time_to_seconds(t):
        h, m, s = t.replace(",", ":").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    def parse_srt(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")

        subs = []
        current = None

        for line in lines:

            if "-->" in line:
                start, end = line.split("-->")
                current = {
                    "start": time_to_seconds(start.strip()),
                    "end": time_to_seconds(end.strip()),
                    "text": ""
                }
                subs.append(current)

            elif line.strip() and not line.strip().isdigit():
                if current:
                    current["text"] += line + " "

        return subs

    subtitles = parse_srt(srt_path)

    clips = [video]
    overlays = []

    # -----------------------------
    # 🎯 WORD TIMING SPLIT ENGINE
    # -----------------------------
    for sub in subtitles:

        words = sub["text"].strip().split()
        if not words:
            continue

        duration = sub["end"] - sub["start"]
        word_duration = duration / max(len(words), 1)

        for i, word in enumerate(words):

            start = sub["start"] + (i * word_duration)
            end = start + word_duration

            # highlight effect for each word
            txt = TextClip(
                word,
                fontsize=80,
                color="white",
                stroke_color="black",
                stroke_width=5,
                font="Arial-Bold",
                method="caption",
                size=(900, None)
            ).set_start(start).set_end(end).set_position(("center", "bottom"))

            overlays.append(txt)

    final = CompositeVideoClip([video] + overlays)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30
    )