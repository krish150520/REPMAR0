from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
from pushup import process_frame as pushup_frame, reset as pushup_reset
from paths import DATE_FILE, REPS_FILE, TIME_FILE, SESSION_FILE, PROFILE_FILE



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_card=None
        self.selected_exercise=None
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.current_size = (1280, 720)
        self.resize(1280,720)
        central=QWidget()
        self.setCentralWidget(central)
        main_layout=QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.create_titlebar())
        body=QHBoxLayout()
        body.addWidget(self.create_sidebar())
        body.addWidget(self.create_main())
        main_layout.addLayout(body)

        central.setStyleSheet("""
        QWidget {
          background-color: #0a0a0f;
          color: #f0f0f5;
          font-family: 'Segoe UI';
      }
        QPushButton {
          background-color: #1a1a26;
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 10px;
          padding: 10px 20px;
          color: #f0f0f5;
       }
        QPushButton:hover {
          background-color: rgba(255,255,255,0.05);
          border-color: rgba(255,255,255,0.15);
       }
        /* Accent button */
       QPushButton#startBtn {
          background-color: #e8ff47;
          color: #0a0a0f;
          font-size: 18px;
          font-weight: bold;
          border-radius: 14px;
       }
      QPushButton#startBtn:hover {
          background-color: #d4eb30;
      }
     """)
    def create_sidebar(self):
       sidebar = QWidget()
       sidebar.setFixedWidth(280)
       sidebar.setStyleSheet("background-color: #12121a; border-right: 1px solid rgba(255,255,255,0.07);")
       layout = QVBoxLayout(sidebar)
       layout.setContentsMargins(20, 24, 20, 24)
       layout.setSpacing(8)
   
       # profile
       profile = QFrame()
       profile.setStyleSheet("""
           QFrame {
               background: #1a1a26;
               border-radius: 16px;
               border: 1px solid rgba(255,255,255,0.07);
           }
       """)
       p_layout = QVBoxLayout(profile)
       p_layout.setAlignment(Qt.AlignCenter)
       p_layout.setContentsMargins(16, 20, 16, 20)
       p_layout.setSpacing(8)
   
       # avatar
       self.avatar_lbl = QLabel("KS")
       self.avatar_lbl.setFixedSize(72, 72)
       self.avatar_lbl.setAlignment(Qt.AlignCenter)
       self.avatar_lbl.setCursor(Qt.PointingHandCursor)
       self.avatar_lbl.setStyleSheet("""
           background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
               stop:0 #00e676, stop:1 #c8ff00);
           border-radius: 36px;
           color: #0a0a0a;
           font-size: 22px;
           font-weight: bold;
       """)
       self.avatar_lbl.mousePressEvent = lambda e: self.open_profile_popup()
   
       # name
       self.profile_name_lbl = QLabel("KRISH SHARMA")
       self.profile_name_lbl.setAlignment(Qt.AlignCenter)
       self.profile_name_lbl.setCursor(Qt.PointingHandCursor)
       self.profile_name_lbl.setStyleSheet(
           "font-size: 14px; font-weight: bold; letter-spacing: 1px; color: #ffffff;"
       )
       self.profile_name_lbl.mousePressEvent = lambda e: self.open_profile_popup()
   
       # level badge
       self.level_badge = QLabel("⚡ LEVEL 12 — WARRIOR")
       self.level_badge.setAlignment(Qt.AlignCenter)
       self.level_badge.setStyleSheet("""
           color: #c8ff00;
           background: rgba(200,255,0,0.08);
           border: 1px solid rgba(200,255,0,0.2);
           border-radius: 10px;
           padding: 3px 10px;
           font-size: 10px;
           font-weight: bold;
       """)

       # getting profile data
       try:
           with open(PROFILE_FILE, "r") as f:
               lines = f.read().splitlines()
               self.profile_name_lbl.setText(lines[0].upper() if lines else "USER")
               self.avatar_lbl.setText(lines[1].upper()[:2] if len(lines) > 1 else "US")
       except:
           pass
   
       
       p_layout.addWidget(self.avatar_lbl, alignment=Qt.AlignCenter)
       p_layout.addWidget(self.profile_name_lbl, alignment=Qt.AlignCenter)
       p_layout.addWidget(self.level_badge, alignment=Qt.AlignCenter)

    
       layout.addWidget(profile)
       layout.addSpacing(8)

    #    screen buttons
       for icon, label in [("🏠","Home"),("📅","Records"),("📊","Progress"),("⚙️","Settings")]:
           btn = QPushButton(f"  {icon}  {label}")
           if label == "Records":
               btn.clicked.connect(self.open_records)
           elif label == "Progress":
               btn.clicked.connect(self.open_progress)
           elif label == "Settings":
               btn.clicked.connect(self.open_settings)
           btn.setStyleSheet("""
               QPushButton {
                   text-align: left;
                   padding: 12px;
                   border-radius: 10px;
                   color: #6b6b80;
                   border: 1px solid transparent;
               }
               QPushButton:hover {
                   background: rgba(255,255,255,0.05);
                   color: #f0f0f5;
               }
           """)
           layout.addWidget(btn)
   
       layout.addStretch()

    
       exit_btn = QPushButton("  🚪  Exit")
       exit_btn.setStyleSheet("""
           QPushButton {
               text-align: left;
               padding: 12px;
               border-radius: 10px;
               color: #ff4747;
               border: 1px solid transparent;
           }
           QPushButton:hover { background: rgba(255,71,71,0.06); }
       """)
       exit_btn.clicked.connect(QApplication.quit)
       layout.addWidget(exit_btn)

       return sidebar
    
    def create_exercise_selector(self):
         scroll = QScrollArea()
         scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
         scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
         scroll.setWidgetResizable(True)
         scroll.setStyleSheet("background: transparent; border: none;")

         container = QWidget()
         h_layout = QHBoxLayout(container)
         h_layout.setSpacing(16)

         exercises = [
             ("💪", "bicep curls", "strenght · 30 reps"),
             ("🐼", "push ups", "Strength · 30 reps"),
             ("🧏‍♂️","pull ups","streinght . 10 reps")
         ]

         for emoji, name, meta in exercises:
             card = QFrame()
             card.setFixedWidth(150)
             card.setCursor(Qt.PointingHandCursor)
             card.setStyleSheet("""
                 QFrame {
                     background: #1a1a26;
                     border: 1px solid rgba(255,255,255,0.07);
                     border-radius: 16px;
                     padding: 16px;
                 }
                 QFrame:hover {
                     border-color: rgba(232,255,71,0.3);
                 }
             """)
             card.mousePressEvent = lambda event, c=card,n=name: self.select_card(c,n)

             c_layout = QVBoxLayout(card)

             emoji_lbl = QLabel(emoji)
             emoji_lbl.setStyleSheet("font-size: 28px;")
             name_lbl = QLabel(name)
             name_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #f0f0f5;")
             meta_lbl = QLabel(meta)
             meta_lbl.setStyleSheet("font-size: 11px; color: #6b6b80;")
            
             c_layout.addWidget(emoji_lbl)
             c_layout.addWidget(name_lbl)
             c_layout.addWidget(meta_lbl)
             h_layout.addWidget(card)
            

         scroll.setWidget(container)
        
         return scroll
    

    def create_titlebar(self):
        bar = QWidget()
        bar.setFixedHeight(48)
        bar.setStyleSheet("background:#0a0a0f; border-bottom:1px solid rgba(255,255,255,0.07);")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16,0,16,0)
        title = QLabel("⚡ REPMARO")
        title.setStyleSheet("color:#e8ff47; font-size:16px; font-weight:bold; letter-spacing:3px;")
        layout.addWidget(title)
        layout.addStretch()
        return bar

    def create_main(self):
        main = QWidget()
        layout = QVBoxLayout(main)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(24)

        
        heading = QLabel("READY TO\nCRUSH IT?")
        heading.setStyleSheet("font-size:42px; font-weight:bold; color:#f0f0f5; line-height:1;")
        layout.addWidget(heading)

        # Exercise selector
        layout.addWidget(self.create_exercise_selector())

        # Start button
        start_btn = QPushButton("▶  START WORKOUT")
        start_btn.setObjectName("startBtn")
        start_btn.setFixedHeight(56)
        start_btn.clicked.connect(self.start_workout) 
        layout.addWidget(start_btn)
        
        layout.addStretch()
        return main
    
    def select_card(self, card,exercise_name):
        if self.selected_card:
            self.selected_card.setStyleSheet("""
                QFrame {
                    background: #1a1a26;
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 16px;
                    padding: 16px;
                }
                QFrame:hover { border-color: rgba(232,255,71,0.3); }
            """)
    
        card.setStyleSheet("""
            QFrame {
                background: rgba(232,255,71,0.06);
                border: 1px solid #e8ff47;
                border-radius: 16px;
                padding: 16px;
            }
        """)
        self.selected_card = card
        self.selected_exercise = exercise_name

    def start_workout(self):
         if not self.selected_exercise:
             QMessageBox.warning(self, "No Exercise", "Please select an exercise first!")
             return
         
         
     
         
         exercise_map = {
             "push ups":    self.start_pushups,
             "bicep curls":    self.open_score,
             "pull ups":       self.start_pullups,
             
         }
     
         
         func = exercise_map.get(self.selected_exercise)
         if func:
             func()
    def open_records(self):
        from records import RecordScreen
        self.record_win = QMainWindow()
        self.record_win.setWindowFlag(Qt.FramelessWindowHint)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(RecordScreen(menu_ref=self))  
        scroll.setStyleSheet("border: none; background: #0a0a0a;")
        self.record_win.setCentralWidget(scroll)
        if self.isMaximized():
            self.record_win.showMaximized()
        else:
            self.record_win.resize(self.width(), self.height())
            self.record_win.show()
        self.hide()    

    def total_session(self):
      try:
        with open(SESSION_FILE, "r") as old_data:
            session = int(old_data.read())

      except Exception:
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Popup")
        self.msg.setText("ERROR IN OPENING FILE😭")
        self.msg.exec_()
        session=0
      
      session+=1
      with open(SESSION_FILE,"w") as new_data:
         new_data.write(str(session))
         
    def open_score(self):
        self.total_session()
        from bicep import process_frame, reset
        from score import WorkoutScreen
        reset()
        self.score = WorkoutScreen(exercise_name="Bicep Curls", menu_ref=self)  
        self.score.process_fn = process_frame
        if self.isMaximized():
            self.score.showMaximized()
        else:
            self.score.resize(self.width(), self.height())
            self.score.show()
        self.hide()

    
    def open_progress(self):
        from progress_screen import ProgressScreen
        self.progress = ProgressScreen(menu_ref=self)  
        self.progress.setWindowFlag(Qt.FramelessWindowHint)
        if self.isMaximized():
            self.progress.showMaximized()
        else:
            self.progress.resize(self.width(), self.height())
            self.progress.show()
        self.hide() 
    def start_pushups(self):
        self.total_session()
        from pushup import process_frame, reset
        from pushupscore import WorkoutScreen
        reset()
        self.score = WorkoutScreen(exercise_name="Push Ups", menu_ref=self)  
        self.score.setWindowFlag(Qt.FramelessWindowHint)
        self.score.process_fn = process_frame
        if self.isMaximized() or self.isFullScreen():
            self.score.showMaximized()
        else:
            self.score.resize(self.width(), self.height())
            self.score.show()
        self.hide()
    def start_pullups(self):
        self.total_session()
        from pullup import process_frame, reset
        from score import WorkoutScreen
        reset()
        self.workout_win = WorkoutScreen(exercise_name="Pull Ups", menu_ref=self)  
        self.workout_win.setWindowFlag(Qt.FramelessWindowHint)
        self.workout_win.process_fn = process_frame
        if self.isMaximized() or self.isFullScreen():
            self.workout_win.showMaximized()
        else:
            self.workout_win.resize(self.width(), self.height())
            self.workout_win.show()
        self.hide()    
    def open_settings(self):
        from setting import SettingsScreen
        self.settings = SettingsScreen(menu_ref=self)  
        self.settings.setWindowFlag(Qt.FramelessWindowHint)
        if self.isMaximized():
            self.settings.showMaximized()
        else:
            self.settings.resize(self.width(), self.height())
            self.settings.show()
        self.hide() 



    

    def open_profile_popup(self):
        popup = QDialog(self)
        popup.setWindowTitle("Profile")
        popup.setFixedSize(400, 540)
        popup.setWindowFlag(Qt.FramelessWindowHint) 
        popup.setStyleSheet("""
            QDialog { background: #1e1e2a; }
            QLineEdit {
                background: #141414;
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #c8ff00;
            }
        """)

        layout = QVBoxLayout(popup)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        
        title_row = QHBoxLayout()
        title = QLabel("EDIT PROFILE")
        title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                color: #666680;
                border: none;
                border-radius: 14px;
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(255,68,68,0.15); color: #ff4444; }
        """)
        close_btn.clicked.connect(popup.reject)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(close_btn)
        layout.addLayout(title_row)
    
        
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: rgba(255,255,255,0.07);")
        layout.addWidget(div)

        
        avatar_row = QHBoxLayout()
        avatar_row.setAlignment(Qt.AlignCenter)

        self.avatar_preview = QLabel("KS")
        self.avatar_preview.setFixedSize(80, 80)
        self.avatar_preview.setAlignment(Qt.AlignCenter)
        self.avatar_preview.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #00e676, stop:1 #c8ff00);
            border-radius: 40px;
            color: #0a0a0a;
            font-size: 26px;
            font-weight: bold;
        """)

        
        try:
            with open(PROFILE_FILE, "r") as f:
                lines = f.read().splitlines()
                saved_name     = lines[0] if len(lines) > 0 else "User"
                saved_initials = lines[1] if len(lines) > 1 else "US"
                self.avatar_preview.setText(saved_initials.upper()[:2])
        except:
            saved_name     = "User"
            saved_initials = "US"
    
        avatar_row.addWidget(self.avatar_preview)
        layout.addLayout(avatar_row)

    
        name_lbl = QLabel("DISPLAY NAME")
        name_lbl.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 2px;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name...")
        self.name_input.setText(saved_name)
        self.name_input.setFixedHeight(44)
    
        layout.addWidget(name_lbl)
        layout.addWidget(self.name_input)


        init_lbl = QLabel("AVATAR INITIALS  (max 2 characters)")
        init_lbl.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 2px;")

        self.initials_input = QLineEdit()
        self.initials_input.setPlaceholderText("e.g. KS")
        self.initials_input.setText(saved_initials)
        self.initials_input.setMaxLength(2)
        self.initials_input.setFixedHeight(44)

        self.initials_input.textChanged.connect(
            lambda text: self.avatar_preview.setText(text.upper()[:2])
        )

        layout.addWidget(init_lbl)
        layout.addWidget(self.initials_input)

        level_frame = QFrame()
        level_frame.setStyleSheet("""
        QFrame {
               background: rgba(200,255,0,0.06);
               border: 1px solid rgba(200,255,0,0.2);
               border-radius: 12px;
           }
        """)
        level_layout = QHBoxLayout(level_frame)
        level_layout.setContentsMargins(16, 14, 16, 14)
        level_layout.setSpacing(12)

        # Get level from reps
        try:
            from level_logic import get_level_info
            with open(REPS_FILE, "r") as f:
                total_reps = sum(
                    int(l.strip().split()[-1])
                    for l in f if l.strip()
                )
            _, lvl_title, lvl_emoji, xp_in, xp_need, pct = get_level_info(total_reps)
        except:
            lvl_title  = "BEGINNER"
            lvl_emoji  = "🌱"
            total_reps = 0
            pct        = 0
        emoji_lbl = QLabel(lvl_emoji)
        emoji_lbl.setFixedSize(40, 40)
        emoji_lbl.setAlignment(Qt.AlignCenter)
        emoji_lbl.setStyleSheet("font-size: 26px; background: transparent; border: none;")
        vline = QFrame()
        vline.setFixedWidth(1)
        vline.setStyleSheet("background: rgba(200,255,0,0.15); border: none;")
        text_col = QVBoxLayout()
        text_col.setSpacing(3)
        text_col.setContentsMargins(0, 0, 0, 0)
        lbl_top = QLabel("CURRENT LEVEL")
        lbl_top.setStyleSheet("""
            color: #666680;
            font-size: 9px;
            letter-spacing: 2px;
            background: transparent;
            border: none;
        """) 
        lbl_title = QLabel(lvl_title)
        lbl_title.setStyleSheet("""
         color: #c8ff00;
         font-size: 16px;
         font-weight: bold;
         letter-spacing: 2px;
         background: transparent;
          border: none;
           """)
        lbl_xp = QLabel(f"{total_reps} XP  ·  {pct}% to next level")
        lbl_xp.setStyleSheet("""
            color: #666680;
            font-size: 10px;
            background: transparent;
            border: none;
        """)
        text_col.addWidget(lbl_top)
        text_col.addWidget(lbl_title)
        text_col.addWidget(lbl_xp)

        level_layout.addWidget(emoji_lbl)
        level_layout.addWidget(vline)
        level_layout.addLayout(text_col)
        level_layout.addStretch()
        layout.addWidget(level_frame)
        layout.addStretch()

        # save button 
        save_btn = QPushButton("✓  SAVE PROFILE")
        save_btn.setFixedHeight(48)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #c8ff00;
                color: #0a0a0a;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover { background: #a8d400; }
        """)
        save_btn.clicked.connect(lambda: self.save_profile(popup))
        layout.addWidget(save_btn)

        popup.exec_()


    def save_profile(self, popup):
        name     = self.name_input.text().strip() or "User"
        initials = self.initials_input.text().strip().upper()[:2] or "US"

        # Save to file
        with open(PROFILE_FILE, "w") as f:
            f.write(f"{name}\n{initials}")

        #  Update sidebar live
        self.profile_name_lbl.setText(name.upper())
        self.avatar_lbl.setText(initials)

        popup.accept()
    
        # Success toast
        toast = QLabel("✓  Profile saved!", self)
        toast.setStyleSheet("""
            background: #1e1e2a;
            color: #c8ff00;
            border: 1px solid rgba(200,255,0,0.3);
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: bold;
        """)
        toast.setAlignment(Qt.AlignCenter)
        toast.setFixedSize(200, 44)
        # Center it on screen
        toast.move(
            self.width() // 2 - 100,
            self.height() - 80
        )
        toast.show()
        QTimer.singleShot(2000, toast.deleteLater)    

    def resizeEvent(self, event):
       self.current_size = (self.width(), self.height())
       super().resizeEvent(event)           
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()