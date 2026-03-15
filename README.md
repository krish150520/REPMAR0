# ⚡ Repmaro – AI Workout Rep Tracker

**Repmaro** is a desktop fitness tracking application that uses **computer vision and pose estimation** to automatically detect and count exercise repetitions in real time. The application combines **Python, PyQt5, OpenCV, and MediaPipe** to create an interactive workout tracker with a modern user interface and gamified progress system.

Repmaro helps users stay consistent with their workouts by tracking reps, sessions, streaks, and achievements while providing visual progress feedback.

---

## 🚀 Features

* 🎥 **Real-time Rep Counting**
  Uses **MediaPipe Pose Detection** to track body movements and count exercise repetitions automatically.

* 🏋️ **Multiple Exercises Supported**

  * Push Ups
  * Bicep Curls
  * Pull Ups

* 📊 **Progress Tracking**

  * Total reps
  * Workout sessions
  * Workout streaks
  * Accuracy tracking

* 🎮 **Gamified Progress System**

  * XP system (1 rep = 1 XP)
  * Level progression
  * Achievement badges
  * Streak milestones

* 📅 **Workout History**

  * Records sessions
  * Activity tracking
  * Heatmap-style visualization

* 🎨 **Modern Desktop UI**

  * Built using **PyQt5**
  * Dark theme interface
  * Smooth navigation between screens

---

## 🧠 Technologies Used

* **Python**
* **PyQt5** – Desktop GUI
* **OpenCV** – Video processing
* **MediaPipe** – Pose detection & body tracking
* **NumPy** – Data processing

---

## 📂 Project Structure

```
wotracker/
│
├── menur.py            # Main dashboard
├── progress_screen.py  # Level and badge system
├── records.py          # Workout history
├── score.py            # Workout tracking screen
├── level_logic.py      # Level and achievement logic
│
├── session.txt         # Session data
├── rep_count.txt       # Rep records
├── date.txt            # Workout streak data
```

---

## 🎯 How It Works

1. The camera captures the user performing exercises.
2. **MediaPipe Pose Landmarks** detect body joint positions.
3. Angle calculations determine correct movement patterns.
4. Reps are automatically counted.
5. Workout data is saved and used to update:

   * XP levels
   * achievements
   * streaks
   * progress dashboard

---

## 📸 Screenshots

*(Add screenshots of the UI here)*

* Main Dashboard
* Exercise Selection
* Workout Screen
* Progress & Achievements

---

## 🏆 Future Improvements

* More exercises (Squats, Lunges, Planks)
* Real workout heatmap
* AI form correction feedback
* Workout analytics dashboard
* Mobile companion version

---

## 👨‍💻 Author

**Krish Sharma**

A project focused on combining **computer vision, GUI development, and gamification** to create a smart fitness tracking experience.
