import cv2


def detect_face_centers(video_path, sample_rate=3):
    """
    OpusClip-style SMART sampling face tracker
    (fast + stable + production approach)
    """

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(video_path)

    centers = []

    frame_index = 0
    sampled_index = 0

    print("🚀 Smart face tracking started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_index += 1

        # ONLY process every Nth frame (SPEED BOOST)
        if frame_index % sample_rate != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

            cx = x + w / 2
            cy = y + h / 2

            centers.append((cx, cy))
        else:
            centers.append(None)

        sampled_index += 1

        if sampled_index % 50 == 0:
            print(f"Processed {sampled_index} sampled frames...")

    cap.release()

    print(f"✅ Done. Sampled frames: {sampled_index}")

    return centers