import numpy as np


def smooth_points(points, smoothing=0.2):
    """
    Convert raw face points into smooth camera movement
    (OpusClip-style stabilization)
    """

    smoothed = []
    prev = None

    for p in points:
        if p is None:
            smoothed.append(prev)
            continue

        if prev is None:
            prev = p

        x = prev[0] + smoothing * (p[0] - prev[0])
        y = prev[1] + smoothing * (p[1] - prev[1])

        prev = (x, y)
        smoothed.append(prev)

    return smoothed


def generate_crop_path(face_centers, frame_size, output_size=(1080, 1920)):
    """
    Convert face positions into crop window positions
    """

    w, h = frame_size
    ow, oh = output_size

    crop_path = []

    for p in face_centers:
        if p is None:
            # center fallback
            cx, cy = w / 2, h / 2
        else:
            cx, cy = p

        # convert to top-left crop position
        x = max(0, min(cx - ow / 2, w - ow))
        y = max(0, min(cy - oh / 2, h - oh))

        crop_path.append((int(x), int(y)))

    return crop_path