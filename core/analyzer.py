import re


def find_viral_segments(segments):
    """
    OpusClip-style viral scoring engine
    Works on Whisper segments
    """

    clips = []

    current = None
    score = 0

    for seg in segments:

        text = seg["text"].lower()

        # ---------------------------
        # VIRAL SIGNAL DETECTION
        # ---------------------------

        hook_words = [
            "you need", "secret", "stop", "never", "how to",
            "this is why", "important", "mistake", "warning"
        ]

        engagement_words = [
            "!", "?", "really", "actually", "crazy", "insane"
        ]

        s = 0

        # length bonus (medium speech = better clips)
        length = seg["end"] - seg["start"]
        if 2 <= length <= 15:
            s += 2

        # hook detection
        if any(w in text for w in hook_words):
            s += 3

        # engagement punctuation
        if any(w in text for w in engagement_words):
            s += 1

        # sentence richness
        if len(text.split()) > 8:
            s += 1

        # ---------------------------
        # BUILD CLIP WINDOW
        # ---------------------------

        if current is None:
            current = {
                "start": seg["start"],
                "end": seg["end"],
                "score": s
            }
        else:
            # merge nearby segments
            if seg["start"] - current["end"] < 1.5:
                current["end"] = seg["end"]
                current["score"] += s
            else:
                clips.append(current)
                current = {
                    "start": seg["start"],
                    "end": seg["end"],
                    "score": s
                }

    if current:
        clips.append(current)

    # ---------------------------
    # SORT BY VIRAL SCORE
    # ---------------------------
    clips.sort(key=lambda x: x["score"], reverse=True)

    return clips