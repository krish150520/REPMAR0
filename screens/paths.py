
import os

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STORAGE      = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE, exist_ok=True)

DATE_FILE    = os.path.join(STORAGE, "date.txt")
REPS_FILE    = os.path.join(STORAGE, "rep_count.txt")
TIME_FILE    = os.path.join(STORAGE, "totaltime.txt")
SESSION_FILE = os.path.join(STORAGE, "session.txt")
PROFILE_FILE = os.path.join(STORAGE, "profile.txt")


MODEL_PATH   = os.path.join(BASE_DIR, "model", "pose_landmarker_heavy.task")