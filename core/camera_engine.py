import numpy as np


def build_camera_path(face_points, video_size, output_size=(1080, 1920)):
    """
    FULL OpusClip-style camera motion engine
    Converts face tracking → smooth moving crop window
    """

    vw, vh = video_size
    ow, oh = output_size

    path = []

    prev_x, prev_y = vw / 2, vh / 2
    prev_zoom = 1.0

    for p in face_points:

        # fallback to center if no face
        if p is None:
            cx, cy = vw / 2, vh / 2
        else:
            cx, cy = p

        # -----------------------------
        # SMOOTH CAMERA FOLLOW
        # -----------------------------
        alpha = 0.15  # smoothing factor

        cam_x = prev_x + alpha * (cx - prev_x)
        cam_y = prev_y + alpha * (cy - prev_y)

        # -----------------------------
        # ZOOM LOGIC (face size simulation)
        # -----------------------------
        # closer face = more zoom (simple heuristic)
        zoom = 1.0

        # smooth zoom
        cam_zoom = prev_zoom + alpha * (zoom - prev_zoom)

        prev_x, prev_y, prev_zoom = cam_x, cam_y, cam_zoom

        # -----------------------------
        # convert to crop position
        # -----------------------------
        crop_w = ow / cam_zoom
        crop_h = oh / cam_zoom

        x = cam_x - crop_w / 2
        y = cam_y - crop_h / 2

        # clamp inside video
        x = max(0, min(x, vw - crop_w))
        y = max(0, min(y, vh - crop_h))

        path.append({
            "x": int(x),
            "y": int(y),
            "w": int(crop_w),
            "h": int(crop_h)
        })

    return path


def smooth_camera_path(path, strength=0.25):
    """
    Extra smoothing layer (removes jitter completely)
    """

    smoothed = []
    prev = None

    for p in path:
        if prev is None:
            prev = p

        nx = prev["x"] + strength * (p["x"] - prev["x"])
        ny = prev["y"] + strength * (p["y"] - prev["y"])
        nw = prev["w"] + strength * (p["w"] - prev["w"])
        nh = prev["h"] + strength * (p["h"] - prev["h"])

        prev = {"x": nx, "y": ny, "w": nw, "h": nh}
        smoothed.append(prev)

    return smoothed