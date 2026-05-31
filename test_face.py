import sys
import os

# force project root into path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.face_tracker import detect_face_centers

video = r"C:\Users\muzam\PycharmProjects\AIClipper\input.mp4"

faces = detect_face_centers(video)

print("Frames processed:", len(faces))
print("First 10 values:", faces[:10])