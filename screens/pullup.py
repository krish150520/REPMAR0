import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
from paths import MODEL_PATH



BaseOptions           = python.BaseOptions
PoseLandmarker        = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode     = vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

pose = PoseLandmarker.create_from_options(options)


counter = 0
isdown  = False


def calculate_angle(a, b, c):
    """Standard 3-point angle at joint b"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def check_form_pullup(l_angle, r_angle, stage):
    """
    Back view form checks:
    - Both arms should move together (symmetry)
    - Full extension at bottom
    - Full pull at top (elbow < 90)
    """
    issues = []

    diff = abs(l_angle - r_angle)
    if diff > 25:
        if l_angle > r_angle:
            issues.append("Pull LEFT arm more!")
        else:
            issues.append("Pull RIGHT arm more!")

    if stage == "UP":
        avg = (l_angle + r_angle) / 2
        if avg > 100:
            issues.append("Pull higher — chin over bar!")

    if stage == "DOWN":
        avg = (l_angle + r_angle) / 2
        if avg < 140:
            issues.append("Extend arms fully at bottom!")

    if issues:
        return False, issues[0]
    return True, "Good Form!"


def process_frame(frame):
    global counter, isdown

    stage      = "DOWN"
    bar_value  = 0
    is_correct = True
    feedback   = ""

    frame_timestamp_ms = int(time.time() * 1000)

    rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result   = pose.detect_for_video(mp_image, frame_timestamp_ms)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]
        h, w, _   = frame.shape

        l_shoulder = [landmarks[11].x * w, landmarks[11].y * h]
        l_elbow    = [landmarks[13].x * w, landmarks[13].y * h]
        l_wrist    = [landmarks[15].x * w, landmarks[15].y * h]

        r_shoulder = [landmarks[12].x * w, landmarks[12].y * h]
        r_elbow    = [landmarks[14].x * w, landmarks[14].y * h]
        r_wrist    = [landmarks[16].x * w, landmarks[16].y * h]

        l_hip = [landmarks[23].x * w, landmarks[23].y * h]
        r_hip = [landmarks[24].x * w, landmarks[24].y * h]

        l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
        avg_angle = (l_angle + r_angle) / 2

        bar_value = int(np.interp(avg_angle, [60, 170], [100, 0]))
        bar_value = max(0, min(100, bar_value))

        if avg_angle > 155:
            stage  = "DOWN"
            isdown = True

        if avg_angle < 90 and isdown:
            stage   = "UP"
            counter += 1
            isdown  = False

        is_correct, feedback = check_form_pullup(l_angle, r_angle, stage)

        pts_l = [l_shoulder, l_elbow, l_wrist]
        for pt in pts_l:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 7, (71, 255, 232), -1)
        cv2.line(frame, tuple(map(int, l_shoulder)), tuple(map(int, l_elbow)), (71,255,232), 3)
        cv2.line(frame, tuple(map(int, l_elbow)),    tuple(map(int, l_wrist)),  (71,255,232), 3)

        pts_r = [r_shoulder, r_elbow, r_wrist]
        for pt in pts_r:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 7, (200, 255, 0), -1)
        cv2.line(frame, tuple(map(int, r_shoulder)), tuple(map(int, r_elbow)), (200,255,0), 3)
        cv2.line(frame, tuple(map(int, r_elbow)),    tuple(map(int, r_wrist)),  (200,255,0), 3)

        cv2.circle(frame, (int(l_hip[0]), int(l_hip[1])), 5, (180, 180, 180), -1)
        cv2.circle(frame, (int(r_hip[0]), int(r_hip[1])), 5, (180, 180, 180), -1)
        cv2.line(frame, tuple(map(int, l_hip)), tuple(map(int, r_hip)), (180,180,180), 2)

        cv2.line(frame, tuple(map(int, l_shoulder)), tuple(map(int, r_shoulder)), (100,100,255), 2)

        cv2.putText(frame, f"L:{int(l_angle)}",
                    (int(l_elbow[0]) + 10, int(l_elbow[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (71,255,232), 2)
        cv2.putText(frame, f"R:{int(r_angle)}",
                    (int(r_elbow[0]) + 10, int(r_elbow[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,255,0), 2)
        cv2.putText(frame, f"Avg:{int(avg_angle)}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        color = (0, 200, 0) if is_correct else (0, 0, 255)
        text  = "GOOD FORM" if is_correct else feedback
        cv2.rectangle(frame, (10, 10), (420, 55), (0,0,0), -1)
        cv2.putText(frame, text, (15, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        print(f"L:{l_angle:.1f} R:{r_angle:.1f} Avg:{avg_angle:.1f} | {stage} | reps:{counter} | {'✓' if is_correct else feedback}")

    return frame, counter, stage, bar_value, is_correct, feedback


def reset():
    global counter, isdown
    counter = 0
    isdown  = False