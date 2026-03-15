from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from paths import DATE_FILE, REPS_FILE, TIME_FILE, SESSION_FILE, PROFILE_FILE



class SettingsScreen(QWidget):
    def __init__(self,menu_ref=None):
        super().__init__()
        self.menu_ref = menu_ref
        self.setStyleSheet("background-color: #0a0a0a;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.create_navbar())

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(48, 40, 48, 48)
        cl.setSpacing(28)

        cl.addWidget(self.create_header())
        cl.addWidget(self.create_danger_zone())
        cl.addStretch()

        layout.addWidget(content)

    
    def create_navbar(self):
        nav = QWidget()
        nav.setFixedHeight(56)
        nav.setStyleSheet("""
            background: #0a0a0a;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        """)
        h = QHBoxLayout(nav)
        h.setContentsMargins(24, 0, 24, 0)

        app_name = QLabel("⚡ REPMARO")
        app_name.setStyleSheet("""
            color: #c8ff00;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 3px;
        """)

        page_lbl = QLabel("SETTINGS")
        page_lbl.setStyleSheet("color: #666680; font-size: 11px; letter-spacing: 3px;")

        back_btn = QPushButton("← Back to Menu")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFixedHeight(34)
        back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #666680;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 8px;
                padding: 0 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ffffff;
                border-color: rgba(255,255,255,0.2);
                background: rgba(255,255,255,0.04);
            }
        """)
        back_btn.clicked.connect(self.go_back_to_menu)

        h.addWidget(app_name)
        h.addStretch()
        h.addWidget(page_lbl)
        h.addStretch()
        h.addWidget(back_btn)
        return nav

    
    def create_header(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        tag = QLabel("PREFERENCES")
        tag.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 3px;")

        title = QLabel("SETTINGS")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 46px;
            font-weight: bold;
        """)

        sub = QLabel("Manage your app data and preferences")
        sub.setStyleSheet("color: #666680; font-size: 13px;")

        layout.addWidget(tag)
        layout.addWidget(title)
        layout.addWidget(sub)
        return w

    
    def create_danger_zone(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # section title
        title_row = QHBoxLayout()
        title = QLabel("DATA MANAGEMENT")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        danger_tag = QLabel("⚠ DANGER ZONE")
        danger_tag.setStyleSheet("""
            color: #ff4444;
            font-size: 10px;
            font-weight: bold;
            background: rgba(255,68,68,0.08);
            border: 1px solid rgba(255,68,68,0.2);
            border-radius: 6px;
            padding: 3px 10px;
            letter-spacing: 1px;
        """)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(danger_tag)
        layout.addLayout(title_row)

        # delete options 
        delete_options = [
            (
                "🗑️",
                "Clear Workout History",
                "Deletes all dates from date.txt — your heatmap will be reset",
                [DATE_FILE],
                "#ff4444",
            ),
            (
                "📊",
                "Clear Rep Records",
                "Deletes all rep counts from rep_count.txt — XP and levels will reset",
                [REPS_FILE],
                "#ff6b35",
            ),
            (
                "⏱️",
                "Clear Total Time",
                "Resets your total workout time back to zero",
                [TIME_FILE],
                "#ff9f47",
            ),
            (
                "🔢",
                "Clear Session Count",
                "Resets your total session counter back to zero",
                [SESSION_FILE],
                "#ffcc00",
            ),
            (
                "💣",
                "Reset ALL Data",
                "Completely wipes everything — reps, dates, time, sessions. Cannot be undone!",
                [DATE_FILE, REPS_FILE, TIME_FILE, SESSION_FILE],
                "#ff4444",
            ),
        ]

        for emoji, title_txt, desc, files, accent in delete_options:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: #1e1e2a;
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 14px;
                }}
                QFrame:hover {{
                    border-color: {accent}44;
                    background: #22222e;
                }}
            """)

            row = QHBoxLayout(card)
            row.setContentsMargins(20, 16, 20, 16)
            row.setSpacing(16)

            # icon
            icon_lbl = QLabel(emoji)
            icon_lbl.setStyleSheet("font-size: 26px;")
            icon_lbl.setFixedWidth(40)

            # text
            text_col = QVBoxLayout()
            text_col.setSpacing(3)
            t = QLabel(title_txt)
            t.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
            d = QLabel(desc)
            d.setStyleSheet("color: #666680; font-size: 11px;")
            d.setWordWrap(True)
            text_col.addWidget(t)
            text_col.addWidget(d)

            # delete button
            del_btn = QPushButton("Delete")
            del_btn.setFixedSize(80, 34)
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255,68,68,0.08);
                    color: {accent};
                    border: 1px solid {accent}55;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {accent}22;
                    border-color: {accent};
                }}
            """)
            del_btn.clicked.connect(
                lambda checked, f=files, t=title_txt: self.confirm_delete(f, t)
            )

            row.addWidget(icon_lbl)
            row.addLayout(text_col)
            row.addStretch()
            row.addWidget(del_btn)
            layout.addWidget(card)

        return section

    
    def confirm_delete(self, files, action_name):
        popup = QDialog(self)
        popup.setWindowTitle("Confirm Delete")
        popup.setFixedSize(380, 220)
        popup.setStyleSheet("QDialog { background: #1e1e2a; }")

        layout = QVBoxLayout(popup)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)

        
        title = QLabel(f"⚠️  Delete {action_name}?")
        title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;")

        desc = QLabel("This action cannot be undone.\nAll related data will be permanently deleted.")
        desc.setStyleSheet("color: #666680; font-size: 12px;")
        desc.setWordWrap(True)

        
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: rgba(255,255,255,0.07);")

        # buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                color: #666680;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover { color: #ffffff; background: rgba(255,255,255,0.1); }
        """)
        cancel_btn.clicked.connect(popup.reject)

        confirm_btn = QPushButton("Yes, Delete")
        confirm_btn.setFixedHeight(40)
        confirm_btn.setCursor(Qt.PointingHandCursor)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,68,68,0.15);
                color: #ff4444;
                border: 1px solid rgba(255,68,68,0.3);
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background: rgba(255,68,68,0.25); border-color: #ff4444; }
        """)
        confirm_btn.clicked.connect(lambda: self.do_delete(files, popup))

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(confirm_btn)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(div)
        layout.addStretch()
        layout.addLayout(btn_row)

        popup.exec_()

    # delete 
    def do_delete(self, files, popup):
        popup.accept()

        reset_values = {
            DATE_FILE:      "",
            REPS_FILE: "",
            TIME_FILE: "0",
            SESSION_FILE:   "0",
        }

        for filename in files:
            try:
                with open(filename, "w") as f:
                    f.write(reset_values.get(filename, ""))
            except Exception as e:
                print(f"Error clearing {filename}: {e}")

        self.show_success(files)

    
    def show_success(self, files):
        toast = QDialog(self)
        toast.setWindowTitle("")
        toast.setFixedSize(320, 120)
        toast.setStyleSheet("QDialog { background: #1e1e2a; border-radius: 12px; }")

        layout = QVBoxLayout(toast)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setAlignment(Qt.AlignCenter)

        msg = QLabel("✓  Data cleared successfully!")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("color: #c8ff00; font-size: 15px; font-weight: bold;")

        sub = QLabel(f"Cleared: {', '.join(os.path.basename(f) for f in files)}")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #666680; font-size: 11px;")

        layout.addWidget(msg)
        layout.addWidget(sub)

        
        QTimer.singleShot(2000, toast.accept)
        toast.exec_()


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



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-family: 'Segoe UI'; color: #ffffff; background: #0a0a0a; }")
    w = QMainWindow()
    w.resize(1280, 720)
    w.setWindowTitle("Settings")
    w.setCentralWidget(SettingsScreen())
    w.show()
    sys.exit(app.exec_())