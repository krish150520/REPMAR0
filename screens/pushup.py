import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
from paths import MODEL_PATH


BaseOptions        = python.BaseOptions
PoseLandmarker     = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode  = vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

pose = PoseLandmarker.create_from_options(options)


counter = 0
isdown  = False


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


def check_form_pushup(angle, stage):
    """Returns (is_correct, feedback)"""

    
    if stage == "DOWN" and angle > 80:
        return False, "Go lower!"

    
    if stage == "DOWN" and angle < 40:
        return False, "Too deep / elbows flaring!"

    return True, "Good Form!"


def process_frame(frame):
    global counter, isdown

    stage      = "UP"
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

        l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

        
        angle = (l_angle + r_angle) / 2

        
        bar_value = int(np.interp(angle, [70, 160], [0, 100]))
        bar_value = max(0, min(100, bar_value))

        
        if angle > 150:
            stage  = "UP"
            isdown = True

        
        if angle < 73 and isdown:
            stage   = "DOWN"
            counter += 1
            isdown  = False

        
        is_correct, feedback = check_form_pushup(angle, stage)

        
        
        for pt in [l_shoulder, l_elbow, l_wrist]:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 6, (71, 255, 232), -1)
        cv2.line(frame, tuple(map(int, l_shoulder)), tuple(map(int, l_elbow)), (71,255,232), 2)
        cv2.line(frame, tuple(map(int, l_elbow)),    tuple(map(int, l_wrist)),  (71,255,232), 2)

        
        for pt in [r_shoulder, r_elbow, r_wrist]:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 6, (200, 255, 0), -1)
        cv2.line(frame, tuple(map(int, r_shoulder)), tuple(map(int, r_elbow)), (200,255,0), 2)
        cv2.line(frame, tuple(map(int, r_elbow)),    tuple(map(int, r_wrist)),  (200,255,0), 2)


        cv2.putText(frame, f"L:{int(l_angle)}",
                    (int(l_elbow[0])+10, int(l_elbow[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (71,255,232), 2)
        cv2.putText(frame, f"R:{int(r_angle)}",
                    (int(r_elbow[0])+10, int(r_elbow[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,255,0), 2)

        color = (0, 255, 0) if is_correct else (0, 0, 255)
        text  = "✓ CORRECT" if is_correct else f"✗ {feedback}"
        cv2.rectangle(frame, (10, 10), (380, 55), (0,0,0), -1)
        cv2.putText(frame, text, (15, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        print(f"L:{l_angle:.1f} R:{r_angle:.1f} | {stage} | reps:{counter} | {'✓' if is_correct else feedback}")

    return frame, counter, stage, bar_value, is_correct, feedback


def reset():
    global counter, isdown
    counter = 0
    isdown  = False