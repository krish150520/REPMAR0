# progress_screen.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from level_logic import get_level_info, get_all_badges_with_status, LEVELS
from datetime import datetime
from paths import DATE_FILE, REPS_FILE, TIME_FILE, SESSION_FILE, PROFILE_FILE



class ProgressScreen(QWidget):
    def __init__(self, stats=None,menu_ref=None):
        super().__init__()
        self.menu_ref = menu_ref
        with open(SESSION_FILE,"r") as sessioncount:
            c=int(sessioncount.read())
        with open(REPS_FILE,"r") as repcount: 
            total_reps=0
            for line in repcount:
                parts = line.strip().split()
                reps = int(parts[-1])   
                total_reps += reps
        # print(total_reps)        
        with open(DATE_FILE,"r") as date:
            dates = [line.strip() for line in date]
            best_streak = self.calculate_streak(dates)

        self.stats = stats or {
            "total_reps":      total_reps,
            "total_sessions":  c,
            "best_streak":     best_streak,
            "best_accuracy":   100,
        }

        self.setStyleSheet("background-color: #0a0a0a;")

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            border: none;
            background: transparent;
            QScrollBar:vertical {
                background: transparent; width: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.1);
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0px; }
        """)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(48, 36, 48, 48)
        layout.setSpacing(32)

        layout.addWidget(self.create_header())
        layout.addWidget(self.create_level_card())
        layout.addWidget(self.create_level_roadmap())
        layout.addWidget(self.create_badges_section())
        layout.addStretch()

        scroll.setWidget(content)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def create_header(self):
         w = QWidget()
         layout = QVBoxLayout(w)
         layout.setContentsMargins(0, 0, 0, 0)
         layout.setSpacing(12)

         top_row = QHBoxLayout()

    # Back button
         back_btn = QPushButton("← MENU")
         back_btn.setFixedSize(90, 32)
         back_btn.setCursor(Qt.PointingHandCursor)
         back_btn.setStyleSheet("""
             QPushButton {
                 background: transparent;
                 color: #666680;
                 border: 1px solid rgba(255,255,255,0.07);
                 border-radius: 8px;
                 font-size: 12px;
                 font-weight: bold;
             }
             QPushButton:hover {
                 color: #ffffff;
                 border-color: rgba(255,255,255,0.2);
             }
         """)
         back_btn.clicked.connect(self.go_back_to_menu)

         total_reps    = self.stats["total_reps"]
         total_sessions = self.stats["total_sessions"]
         best_streak   = self.stats["best_streak"]

         chips_row = QHBoxLayout()
         chips_row.setSpacing(8)

         for chip_icon, chip_val, chip_lbl in [
             ("⚡", f"{total_reps} XP",       "Total XP"),
             ("🏋️", f"{total_sessions}",      "Sessions"),
             ("🔥", f"{best_streak} days",    "Best Streak"),
         ]:
             chip = QFrame()
             chip.setStyleSheet("""
                 QFrame {
                     background: #1e1e2a;
                     border: 1px solid rgba(255,255,255,0.07);
                     border-radius: 10px;
                 }
             """)
             chip_layout = QHBoxLayout(chip)
             chip_layout.setContentsMargins(12, 8, 12, 8)
             chip_layout.setSpacing(8)
     
             icon_l = QLabel(chip_icon)
             icon_l.setStyleSheet("font-size: 14px;")
     
             text_col = QVBoxLayout()
             text_col.setSpacing(0)
             val_l = QLabel(chip_val)
             val_l.setStyleSheet("color: #c8ff00; font-size: 13px; font-weight: bold;")
             lbl_l = QLabel(chip_lbl)
             lbl_l.setStyleSheet("color: #666680; font-size: 9px; letter-spacing: 1px;")
             text_col.addWidget(val_l)
             text_col.addWidget(lbl_l)

             chip_layout.addWidget(icon_l)
             chip_layout.addLayout(text_col)
             chips_row.addWidget(chip)

         top_row.addWidget(back_btn)
         top_row.addStretch()
         top_row.addLayout(chips_row)
         layout.addLayout(top_row)

         divider = QFrame()
         divider.setFrameShape(QFrame.HLine)
         divider.setStyleSheet("color: rgba(255,255,255,0.06);")
         layout.addWidget(divider)

         title_row = QHBoxLayout()

         left = QVBoxLayout()
         left.setSpacing(6)
     
         label = QLabel("PROGRESS SYSTEM")
         label.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 3px;")

         title = QLabel("YOUR JOURNEY")
         title.setStyleSheet("""
             color: #ffffff;
             font-size: 46px;
             font-weight: bold;
             letter-spacing: 1px;
         """)

         sub = QLabel("Every rep counts — keep pushing towards your next level")
         sub.setStyleSheet("color: #666680; font-size: 13px;")
     
         left.addWidget(label)
         left.addWidget(title)
         left.addWidget(sub)

         level_idx, lvl_title, lvl_emoji, xp_in, xp_need, pct = get_level_info(
             self.stats["total_reps"]
         )

         badge = QFrame()
         badge.setFixedSize(160, 80)
         badge.setStyleSheet("""
             QFrame {
                 background: rgba(200,255,0,0.06);
                 border: 1px solid rgba(200,255,0,0.25);
                 border-radius: 16px;
             }
         """)
         badge_layout = QVBoxLayout(badge)
         badge_layout.setAlignment(Qt.AlignCenter)
         badge_layout.setSpacing(2)
     
         badge_emoji = QLabel(lvl_emoji)
         badge_emoji.setAlignment(Qt.AlignCenter)
         badge_emoji.setStyleSheet("font-size: 28px;")
     
         badge_title = QLabel(lvl_title)
         badge_title.setAlignment(Qt.AlignCenter)
         badge_title.setStyleSheet("color: #c8ff00; font-size: 12px; font-weight: bold; letter-spacing: 2px;")

         badge_sub = QLabel("CURRENT RANK")
         badge_sub.setAlignment(Qt.AlignCenter)
         badge_sub.setStyleSheet("color: #666680; font-size: 9px; letter-spacing: 1px;")

         badge_layout.addWidget(badge_emoji)
         badge_layout.addWidget(badge_title)
         badge_layout.addWidget(badge_sub)

         title_row.addLayout(left)
         title_row.addStretch()
         title_row.addWidget(badge)
         layout.addLayout(title_row)

         return w

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


    def create_level_card(self):
        total_reps = self.stats["total_reps"]
        level_idx, title, emoji, xp_in_level, xp_needed, pct = get_level_info(total_reps)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #1e1e2a;
                border: 1px solid rgba(200,255,0,0.3);
                border-radius: 20px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        top = QHBoxLayout()

        emoji_lbl = QLabel(emoji)
        emoji_lbl.setStyleSheet("font-size: 52px;")
        emoji_lbl.setFixedWidth(70)

        info = QVBoxLayout()
        current_lbl = QLabel("CURRENT LEVEL")
        current_lbl.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 2px;")
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("""
            color: #c8ff00;
            font-size: 36px;
            font-weight: bold;
            letter-spacing: 3px;
        """)
        info.addWidget(current_lbl)
        info.addWidget(title_lbl)

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        xp_lbl = QLabel(f"{total_reps} XP")
        xp_lbl.setStyleSheet("""
            color: #c8ff00;
            font-size: 32px;
            font-weight: bold;
        """)
        xp_lbl.setAlignment(Qt.AlignRight)
        xp_sub = QLabel("Total Reps = Total XP")
        xp_sub.setStyleSheet("color: #666680; font-size: 11px;")
        xp_sub.setAlignment(Qt.AlignRight)
        right.addWidget(xp_lbl)
        right.addWidget(xp_sub)

        top.addWidget(emoji_lbl)
        top.addLayout(info)
        top.addStretch()
        top.addLayout(right)
        layout.addLayout(top)

        if xp_needed > 0:
            bar_label_row = QHBoxLayout()
            bar_lbl = QLabel("Progress to next level")
            bar_lbl.setStyleSheet("color: #666680; font-size: 11px;")
            bar_val = QLabel(f"{xp_in_level} / {xp_needed} XP")
            bar_val.setStyleSheet("color: #ffffff; font-size: 11px;")
            bar_label_row.addWidget(bar_lbl)
            bar_label_row.addStretch()
            bar_label_row.addWidget(bar_val)
            layout.addLayout(bar_label_row)

            bar_bg = QFrame()
            bar_bg.setFixedHeight(14)
            bar_bg.setStyleSheet("""
                background: rgba(255,255,255,0.06);
                border-radius: 7px;
            """)
            bar_fill = QFrame(bar_bg)
            bar_fill.setFixedHeight(14)
            fill_w = max(14, int((pct / 100) * 800))
            bar_fill.setFixedWidth(fill_w)
            bar_fill.setStyleSheet("""
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #00e676, stop:1 #c8ff00);
                border-radius: 7px;
            """)
            layout.addWidget(bar_bg)

            if level_idx + 1 < len(LEVELS):
                next_title = LEVELS[level_idx + 1][1]
                next_emoji = LEVELS[level_idx + 1][2]
                hint = QLabel(f"Next: {next_emoji} {next_title}  —  {xp_needed - xp_in_level} more reps needed")
                hint.setStyleSheet("color: #666680; font-size: 11px;")
                layout.addWidget(hint)
        else:
            maxed = QLabel("👑 MAX LEVEL REACHED — YOU ARE A LEGEND!")
            maxed.setStyleSheet("color: #c8ff00; font-size: 14px; font-weight: bold;")
            layout.addWidget(maxed)

        return card

    def create_level_roadmap(self):
        total_reps = self.stats["total_reps"]
        level_idx, _, _, _, _, _ = get_level_info(total_reps)

        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("LEVEL ROADMAP")
        title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        layout.addWidget(title)

        road = QHBoxLayout()
        road.setSpacing(8)

        for i, (req, lvl_title, lvl_emoji) in enumerate(LEVELS):
            is_current  = i == level_idx
            is_unlocked = i <= level_idx

            card = QFrame()
            card.setFixedHeight(110)

            if is_current:
                border = "#c8ff00"
                bg     = "rgba(200,255,0,0.08)"
            elif is_unlocked:
                border = "rgba(0,230,118,0.3)"
                bg     = "rgba(0,230,118,0.04)"
            else:
                border = "rgba(255,255,255,0.07)"
                bg     = "#141414"

            card.setStyleSheet(f"""
                QFrame {{
                    background: {bg};
                    border: 1px solid {border};
                    border-radius: 12px;
                }}
            """)

            cl = QVBoxLayout(card)
            cl.setAlignment(Qt.AlignCenter)
            cl.setSpacing(4)

            e_lbl = QLabel(lvl_emoji)
            e_lbl.setAlignment(Qt.AlignCenter)
            e_lbl.setStyleSheet("font-size: 22px;")

            t_lbl = QLabel(lvl_title)
            t_lbl.setAlignment(Qt.AlignCenter)
            t_lbl.setStyleSheet(f"""
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 1px;
                color: {'#c8ff00' if is_current else '#ffffff' if is_unlocked else '#666680'};
            """)

            r_lbl = QLabel(f"{req} XP")
            r_lbl.setAlignment(Qt.AlignCenter)
            r_lbl.setStyleSheet("font-size: 9px; color: #666680;")

            if is_current:
                cur_badge = QLabel("YOU ARE HERE")
                cur_badge.setAlignment(Qt.AlignCenter)
                cur_badge.setStyleSheet("""
                    font-size: 7px;
                    color: #0a0a0a;
                    background: #c8ff00;
                    border-radius: 4px;
                    padding: 2px 4px;
                    font-weight: bold;
                """)
                cl.addWidget(cur_badge)

            if not is_unlocked:
                lock = QLabel("🔒")
                lock.setAlignment(Qt.AlignCenter)
                lock.setStyleSheet("font-size: 14px;")
                cl.addWidget(lock)
            else:
                cl.addWidget(e_lbl)

            cl.addWidget(t_lbl)
            cl.addWidget(r_lbl)
            road.addWidget(card)

        layout.addLayout(road)
        return section

    def create_badges_section(self):
        all_badges = get_all_badges_with_status(self.stats)

        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title_row = QHBoxLayout()
        title = QLabel("ACHIEVEMENTS")
        title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        earned_count = sum(1 for b in all_badges if b["earned"])
        count_lbl = QLabel(f"{earned_count}/{len(all_badges)} Unlocked")
        count_lbl.setStyleSheet("""
            color: #c8ff00;
            font-size: 12px;
            background: rgba(200,255,0,0.1);
            border: 1px solid rgba(200,255,0,0.2);
            border-radius: 10px;
            padding: 4px 12px;
        """)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(count_lbl)
        layout.addLayout(title_row)

        grid = QGridLayout()
        grid.setSpacing(12)

        for i, badge in enumerate(all_badges):
            card = QFrame()
            earned = badge["earned"]

            card.setStyleSheet(f"""
                QFrame {{
                    background: {'#1e1e2a' if earned else '#141414'};
                    border: 1px solid {'rgba(200,255,0,0.25)' if earned else 'rgba(255,255,255,0.05)'};
                    border-radius: 14px;
                }}
            """)

            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 16, 16, 16)
            cl.setAlignment(Qt.AlignCenter)
            cl.setSpacing(6)

            emoji_lbl = QLabel(badge["emoji"] if earned else "🔒")
            emoji_lbl.setAlignment(Qt.AlignCenter)
            emoji_lbl.setStyleSheet("font-size: 28px;")

            name_lbl = QLabel(badge["name"])
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"""
                font-size: 12px;
                font-weight: bold;
                color: {'#ffffff' if earned else '#666680'};
            """)
            name_lbl.setWordWrap(True)

            desc_lbl = QLabel(badge["desc"])
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setStyleSheet("font-size: 10px; color: #666680;")
            desc_lbl.setWordWrap(True)

            if earned:
                tag = QLabel("✓ UNLOCKED")
                tag.setAlignment(Qt.AlignCenter)
                tag.setStyleSheet("""
                    font-size: 9px;
                    color: #00e676;
                    font-weight: bold;
                    letter-spacing: 1px;
                """)
                cl.addWidget(tag)

            cl.addWidget(emoji_lbl)
            cl.addWidget(name_lbl)
            cl.addWidget(desc_lbl)

            card.setToolTip(f"{badge['name']}: {badge['desc']}")
            grid.addWidget(card, i // 4, i % 4)

        layout.addLayout(grid)
        return section
    


    def calculate_streak(self,dates):
        if not dates:
            return 0

        dates = sorted(datetime.strptime(d, "%Y-%m-%d") for d in dates)

        current_streak = 1
        best_streak = 1

        for i in range(1, len(dates)):
            diff = (dates[i] - dates[i-1]).days

            if diff == 1:
                current_streak += 1
            elif diff > 1:
                current_streak = 1

            best_streak = max(best_streak, current_streak)

        return best_streak

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-family: 'Segoe UI'; color: #ffffff; background: #0a0a0a; }")

    test_stats = {
        "total_reps":     87,
        "total_sessions": 7,
        "best_streak":    4,
        "best_accuracy":  92,
    }

    w = QMainWindow()
    w.setWindowTitle("Progress")
    w.resize(1280, 720)
    screen = ProgressScreen(test_stats)
    w.setCentralWidget(screen)
    w.show()
    sys.exit(app.exec_())