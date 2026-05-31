from faster_whisper import WhisperModel


# -----------------------------------------------------
# TRANSCRIPTION
# -----------------------------------------------------
def transcribe_audio(audio_path):
    model = WhisperModel("base")

    segments, _ = model.transcribe(audio_path)

    results = []

    for seg in segments:
        results.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })

    return results


# -----------------------------------------------------
# 🔥 KINETIC ASS SUBTITLES (WORD-STYLE TIKTOK)
# -----------------------------------------------------
def save_ass(segments, output_path):

    def format_time(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        cs = int((t - int(t)) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTok,Arial,56,&H00FFFFFF,&H00000000,&H64000000,-1,0,1,3,0,2,20,20,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = ""

    for seg in segments:

        start = format_time(seg["start"])
        end = format_time(seg["end"])

        words = seg["text"].split()

        # -----------------------------
        # KINETIC STYLE GENERATION
        # -----------------------------
        styled_lines = []

        for i, w in enumerate(words):

            # highlight one word at a time
            line = words.copy()
            line[i] = "{\\b1\\fs70\\c&H00FFFF&}" + w + "{\\r}"

            styled_lines.append(" ".join(line))

        # fallback full sentence
        full = "{\\b1\\fs60}" + seg["text"] + "{\\r}"

        # pick full sentence + fake motion effect
        text = full

        events += f"Dialogue: 0,{start},{end},TikTok,,0,0,0,,{text}\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + events)