from pathlib import Path
import os

from core.audio import extract_audio
from core.transcribe import transcribe_audio, save_ass
from core.analyzer import find_viral_segments
from core.cutter import cut_clip, burn_subtitles


# -----------------------------
# SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / "input.mp4")

os.makedirs("output", exist_ok=True)

MAX_CLIPS = 5
MIN_DURATION = 8
MAX_DURATION = 45


# -----------------------------
# 1. EXTRACT AUDIO
# -----------------------------
print("1. Extracting audio...")
audio_path = extract_audio(video_path)


# -----------------------------
# 2. TRANSCRIBE
# -----------------------------
print("2. Transcribing...")
segments = transcribe_audio(audio_path)

# save ASS subtitles (TikTok style)
ass_path = "output/subtitles.ass"
save_ass(segments, ass_path)


# -----------------------------
# 3. VIRAL SEGMENTS
# -----------------------------
print("3. Finding viral moments...")
clips = find_viral_segments(segments)

print(f"Found {len(clips)} potential clips")


# -----------------------------
# 4. FILTER CLIPS
# -----------------------------
filtered = []

for c in clips:
    duration = c["end"] - c["start"]

    if MIN_DURATION <= duration <= MAX_DURATION:
        filtered.append(c)

    if len(filtered) >= MAX_CLIPS:
        break


# -----------------------------
# 5. CUT + BURN SUBTITLES
# -----------------------------
print("4. Creating viral clips...")

for i, clip in enumerate(filtered):

    raw = f"output/raw_{i}.mp4"
    final = f"output/clip_{i}_viral.mp4"

    print(f"\n🎬 Clip {i}: {clip['start']} → {clip['end']}")

    cut_clip(video_path, clip["start"], clip["end"], raw)

    burn_subtitles(raw, ass_path, final)


print("\n✅ DONE - ALL VIRAL CLIPS GENERATED")
print("🔥 READY FOR TIKTOK / SHORTS / REELS")