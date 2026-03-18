from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import time
from pushup import process_frame, reset
from datetime import date
from paths import DATE_FILE, REPS_FILE, TIME_FILE, SESSION_FILE, PROFILE_FILE


class WorkoutScreen(QWidget):
    def __init__(self, exercise_name="Bicep curls",menu_ref=None):
        super().__init__()
        self.menu_ref = menu_ref
        reset() 
        self.date_record()
        self.exercise_name = exercise_name
        self.rep_count = 0
        self.position = "DOWN"
        self.elapsed = 0
        self.start_time = time.time()
        self.is_running = True

        self.setStyleSheet("background-color: #0a0a0f;")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.resize(1280, 720)

        main = QHBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        main.addWidget(self.create_left_panel(), stretch=1)

        main.addWidget(self.create_camera_panel(), stretch=2)

        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_timer)
        self.clock_timer.start(1000)


    
        self.cap = cv2.VideoCapture(0)
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_frame)
        self.frame_timer.start(30)  

    def create_left_panel(self):
        panel = QWidget()
        panel.setFixedWidth(320)
        panel.setStyleSheet("""
            background-color: #12121a;
            border-right: 1px solid rgba(255,255,255,0.07);
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(28, 32, 28, 32)
        layout.setSpacing(20)

        ex_label = QLabel("EXERCISE")
        ex_label.setStyleSheet("color: #6b6b80; font-size: 10px; letter-spacing: 2px;")

        ex_name = QLabel(self.exercise_name.upper())
        ex_name.setStyleSheet("""
            color: #e8ff47;
            font-size: 26px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        ex_name.setWordWrap(True)

        layout.addWidget(ex_label)
        layout.addWidget(ex_name)

        layout.addWidget(self.make_divider())

        layout.addWidget(self.make_section_label("REP COUNT"))
        rep_card = QFrame()
        rep_card.setStyleSheet("""
            QFrame {
                background: #1a1a26;
                border: 1px solid rgba(232,255,71,0.2);
                border-radius: 16px;
            }
        """)
        rep_layout = QVBoxLayout(rep_card)
        rep_layout.setAlignment(Qt.AlignCenter)
        rep_layout.setContentsMargins(20, 24, 20, 24)

        self.rep_label = QLabel(str(self.rep_count))
        self.rep_label.setAlignment(Qt.AlignCenter)
        self.rep_label.setStyleSheet("""
            color: #e8ff47;
            font-size: 80px;
            font-weight: bold;
        """)

        reps_sub = QLabel("reps completed")
        reps_sub.setAlignment(Qt.AlignCenter)
        reps_sub.setStyleSheet("color: #6b6b80; font-size: 12px;")

        rep_layout.addWidget(self.rep_label)
        rep_layout.addWidget(reps_sub)
        layout.addWidget(rep_card)

        layout.addWidget(self.make_section_label("POSITION"))
        pos_card = QFrame()
        pos_card.setStyleSheet("""
            QFrame {
                background: #1a1a26;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 16px;
            }
        """)
        pos_layout = QVBoxLayout(pos_card)
        pos_layout.setAlignment(Qt.AlignCenter)
        pos_layout.setContentsMargins(20, 20, 20, 20)

        self.pos_label = QLabel(self.position)
        self.pos_label.setAlignment(Qt.AlignCenter)
        self.pos_label.setStyleSheet("""
            color: #47ffe8;
            font-size: 36px;
            font-weight: bold;
            letter-spacing: 4px;
        """)

        self.pos_bar = QProgressBar()
        self.pos_bar.setRange(0, 100)
        self.pos_bar.setValue(0)
        self.pos_bar.setTextVisible(False)
        self.pos_bar.setFixedHeight(8)
        self.pos_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.06);
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #47ffe8, stop:1 #e8ff47);
                border-radius: 4px;
            }
        """)

        pos_layout.addWidget(self.pos_label)
        pos_layout.addWidget(self.pos_bar)
        layout.addWidget(pos_card)

        layout.addWidget(self.make_section_label("DURATION"))
        timer_card = QFrame()
        timer_card.setStyleSheet("""
            QFrame {
                background: #1a1a26;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 16px;
            }
        """)
        timer_layout = QHBoxLayout(timer_card)
        timer_layout.setContentsMargins(20, 16, 20, 16)

        clock_icon = QLabel("⏱️")
        clock_icon.setStyleSheet("font-size: 24px;")

        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet("""
            color: #f0f0f5;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        timer_layout.addWidget(clock_icon)
        timer_layout.addWidget(self.timer_label)
        timer_layout.addStretch()
        layout.addWidget(timer_card)

        layout.addStretch()

        stop_btn = QPushButton("⏹  STOP WORKOUT")
        stop_btn.setFixedHeight(52)
        stop_btn.setCursor(Qt.PointingHandCursor)
        stop_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,71,71,0.1);
                color: #ff4747;
                border: 1px solid rgba(255,71,71,0.3);
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: rgba(255,71,71,0.2);
                border-color: #ff4747;
            }
        """)
        layout.addWidget(self.make_section_label("FORM"))
        self.form_label = QLabel("✓  GOOD FORM")
        self.form_label.setAlignment(Qt.AlignCenter)
        self.form_label.setFixedHeight(48)
        self.form_label.setStyleSheet("""
            color: #47ff88;
            font-size: 14px;
            font-weight: bold;
            background: rgba(71,255,136,0.08);
            border: 1px solid rgba(71,255,136,0.25);
            border-radius: 10px;
            padding: 8px;
        """)
        layout.addWidget(self.form_label)
        stop_btn.clicked.connect(self.stop_workout)
        layout.addWidget(stop_btn)

        return panel

    def create_camera_panel(self):
        panel = QWidget()
        panel.setStyleSheet("background-color: #0a0a0f;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Top label
        top_row = QHBoxLayout()
        cam_label = QLabel("📷  LIVE FEED")
        cam_label.setStyleSheet("color: #6b6b80; font-size: 11px; letter-spacing: 2px;")
        self.status_dot = QLabel("● RECORDING")
        self.status_dot.setStyleSheet("color: #ff4747; font-size: 11px; font-weight: bold;")
        top_row.addWidget(cam_label)
        top_row.addStretch()
        top_row.addWidget(self.status_dot)
        layout.addLayout(top_row)

        # Camera feed label
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("""
            background: #1a1a26;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 20px;
        """)
        self.camera_label.setMinimumSize(640, 480)
        layout.addWidget(self.camera_label, stretch=1)

        return panel

    def make_section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #6b6b80; font-size: 10px; letter-spacing: 2px;")
        return lbl

    def make_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: rgba(255,255,255,0.07);")
        return line

    def update_timer(self):
        if not self.is_running:
            return
        self.elapsed = int(time.time() - self.start_time)
        mins = self.elapsed // 60
        secs = self.elapsed % 60
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        annotated_frame, reps, stage, bar_value, is_correct, feedback = process_frame(frame)
        self.update_stats(reps, stage, bar_value, is_correct, feedback)

        rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img).scaled(
            self.camera_label.width(),
            self.camera_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.camera_label.setPixmap(pixmap)

    def update_stats(self, rep_count, position, bar_value=0, is_correct=True, feedback=""):
          self.rep_count = rep_count
          self.position = position

          self.rep_label.setText(str(rep_count))

          self.pos_label.setText(position)
          if position == "UP":
              self.pos_label.setStyleSheet("""
                  color: #e8ff47;
                  font-size: 36px;
                  font-weight: bold;
                  letter-spacing: 4px;
              """)
          else:
              self.pos_label.setStyleSheet("""
                  color: #47ffe8;
                  font-size: 36px;
                  font-weight: bold;
                  letter-spacing: 4px;
              """)
      
          self.pos_bar.setValue(bar_value)

          if is_correct:
              self.form_label.setText("✓  GOOD FORM")
              self.form_label.setStyleSheet("""
                  color: #47ff88;
                  font-size: 14px;
                  font-weight: bold;
                  background: rgba(71,255,136,0.08);
                  border: 1px solid rgba(71,255,136,0.25);
                  border-radius: 10px;
                  padding: 8px;
              """)
          else:
              self.form_label.setText(f"✗  {feedback}")
              self.form_label.setStyleSheet("""
                  color: #ff4747;
                  font-size: 14px;
                  font-weight: bold;
                  background: rgba(255,71,71,0.08);
                  border: 1px solid rgba(255,71,71,0.25);
                  border-radius: 10px;
                  padding: 8px;
              """)

    def stop_workout(self):
          self.is_running = False
          self.frame_timer.stop()
          self.clock_timer.stop()
          self.cap.release()
          self.save_total_time()   
          self.count_reps()        
          self.show_summary()    

    def show_summary(self):
           popup = QDialog(self)
           popup.setWindowTitle("Workout Summary")
           popup.setFixedSize(460, 420)  
           popup.setStyleSheet("""
               QDialog {
                   background: #0a0a0a;
               }
           """)

           layout = QVBoxLayout(popup)
           layout.setContentsMargins(36, 32, 36, 32)
           layout.setSpacing(16)

    # Title
           title = QLabel("🏆 WORKOUT COMPLETE!")
           title.setAlignment(Qt.AlignCenter)
           title.setStyleSheet("color: #c8ff00; font-size: 22px; font-weight: bold; letter-spacing: 2px;")
           layout.addWidget(title)

           sub = QLabel(self.exercise_name.upper())
           sub.setAlignment(Qt.AlignCenter)
           sub.setStyleSheet("color: #666680; font-size: 13px; letter-spacing: 1px;")
           layout.addWidget(sub)

           layout.addWidget(self.make_divider())

           # Stats grid
           stats_grid = QGridLayout()
           stats_grid.setSpacing(12)

           mins = self.elapsed // 60
           secs = self.elapsed % 60
       
           summary_stats = [
               ("💪", "REPS",      str(self.rep_count)),
               ("⏱️", "DURATION",  f"{mins:02d}:{secs:02d}"),
               ("🔥", "CALORIES",  f"~{self.rep_count * 5} kcal"),
               ("⚡", "INTENSITY", "HIGH" if self.rep_count > 15 else "MODERATE"),
           ]
       
           for i, (icon, label, val) in enumerate(summary_stats):
               card = QFrame()
               card.setFixedHeight(100)  
               card.setStyleSheet("""
                   QFrame {
                       background: #1e1e2a;
                       border: 1px solid rgba(255,255,255,0.07);
                       border-radius: 12px;
                   }
               """)
               cl = QVBoxLayout(card)
               cl.setContentsMargins(16, 12, 16, 12)
               cl.setAlignment(Qt.AlignCenter)
               cl.setSpacing(4)

        
               icon_lbl = QLabel(icon)
               icon_lbl.setAlignment(Qt.AlignCenter)
               icon_lbl.setStyleSheet("font-size: 20px;")

               v = QLabel(val)
               v.setAlignment(Qt.AlignCenter)
               v.setStyleSheet("color: #c8ff00; font-size: 20px; font-weight: bold;")
       
               l = QLabel(label)
               l.setAlignment(Qt.AlignCenter)
               l.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 1px;")
       
               cl.addWidget(icon_lbl)  
               cl.addWidget(v)
               cl.addWidget(l)

               stats_grid.addWidget(card, i // 2, i % 2)

           layout.addLayout(stats_grid)

           # Close button
           close_btn = QPushButton("✓  BACK TO MENU")
           close_btn.setFixedHeight(48)
           close_btn.setCursor(Qt.PointingHandCursor)
           close_btn.setStyleSheet("""
               QPushButton {
                   background: #c8ff00;
                   color: #0a0a0a;
                   border: none;
                   border-radius: 12px;
                   font-size: 15px;
                   font-weight: bold;
                   letter-spacing: 1px;
               }
               QPushButton:hover { background: #a8d400; }
           """)
           close_btn.clicked.connect(popup.accept)
           close_btn.clicked.connect(self.go_back_to_menu)
           layout.addWidget(close_btn)

           popup.exec_()
    def go_back_to_menu(self):
        if self.menu_ref:
            if self.isMaximized():
                self.menu_ref.showMaximized()
            else:
                self.menu_ref.resize(self.width(), self.height())
                self.menu_ref.show()
            self.close()
        else:
            from menur import MainWindow
            self.menu = MainWindow()
            self.menu.show()
            self.close()
    def resizeEvent(self, event):
       self.current_size = (self.width(), self.height())
       super().resizeEvent(event)  

    def save_total_time(self):
         try:
             with open(TIME_FILE, "r") as f:
                 total_time = int(f.read())
         except:
             total_time = 0 
     
         total_time += self.elapsed   

         with open(TIME_FILE, "w") as f:
             f.write(str(total_time))

    def count_reps(self):

        with open(REPS_FILE,"a") as kinerepmaremittr:
            kinerepmaremittr.write(f"{self.exercise_name} {self.rep_count}\n")
    def date_record(self):    
        today=date.today()
        print(today)
        aajdidateehegioye=str(today)
        with open(DATE_FILE,"a") as aajdidateoye:
            aajdidateoye.write(f"{aajdidateehegioye}\n")
    # def go_back_to_menu(self):
    #    from menur import MainWindow
    #    self.menu = MainWindow()
    #    self.menu.show()
    #    self.close()  

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = WorkoutScreen("Push Ups")
    w.show()
    sys.exit(app.exec_())
