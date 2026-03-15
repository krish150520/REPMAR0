import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
from paths import MODEL_PATH


BaseOptions = python.BaseOptions
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

pose = PoseLandmarker.create_from_options(options)

counter = 0
isdown = False


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def process_frame(frame):
    global counter, isdown

    stage = "DOWN"
    bar_value = 0

    frame_timestamp_ms = int(time.time() * 1000)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = pose.detect_for_video(mp_image, frame_timestamp_ms)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]
        h, w, _ = frame.shape

        l_shoulder = [landmarks[11].x * w, landmarks[11].y * h]
        l_elbow    = [landmarks[13].x * w, landmarks[13].y * h]
        l_wrist    = [landmarks[15].x * w, landmarks[15].y * h]

        r_shoulder = [landmarks[12].x * w, landmarks[12].y * h]
        r_elbow    = [landmarks[14].x * w, landmarks[14].y * h]
        r_wrist    = [landmarks[16].x * w, landmarks[16].y * h]

        l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

        angle = (l_angle + r_angle) / 2

        bar_value = int(np.interp(angle, [40, 160], [100, 0]))
        bar_value = max(0, min(100, bar_value))

        if angle > 150:
            stage = "DOWN"
            isdown = True

        if angle < 50 and isdown:
            stage = "UP"
            counter += 1
            isdown = False

        for pt in [l_shoulder, l_elbow, l_wrist]:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 6, (71, 255, 232), -1)
        cv2.line(frame, (int(l_shoulder[0]), int(l_shoulder[1])),
                         (int(l_elbow[0]),   int(l_elbow[1])),   (71,255,232), 2)
        cv2.line(frame, (int(l_elbow[0]),    int(l_elbow[1])),
                         (int(l_wrist[0]),   int(l_wrist[1])),   (71,255,232), 2)

        for pt in [r_shoulder, r_elbow, r_wrist]:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 6, (232, 255, 71), -1)
        cv2.line(frame, (int(r_shoulder[0]), int(r_shoulder[1])),
                         (int(r_elbow[0]),   int(r_elbow[1])),   (232,255,71), 2)
        cv2.line(frame, (int(r_elbow[0]),    int(r_elbow[1])),
                         (int(r_wrist[0]),   int(r_wrist[1])),   (232,255,71), 2)

        cv2.putText(frame, f"L: {int(l_angle)}",
                    (int(l_elbow[0]) + 10, int(l_elbow[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (71, 255, 232), 2)
        cv2.putText(frame, f"R: {int(r_angle)}",
                    (int(r_elbow[0]) + 10, int(r_elbow[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (232, 255, 71), 2)

        print(f"L_angle: {l_angle:.1f} | R_angle: {r_angle:.1f} | Counter: {counter} | Stage: {stage}")

    return frame, counter, stage, bar_value


def reset():
    global counter, isdown
    counter = 0
    isdown = False
