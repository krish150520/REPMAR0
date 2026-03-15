from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import date, timedelta
from paths import DATE_FILE, REPS_FILE, TIME_FILE, SESSION_FILE, PROFILE_FILE



class RecordScreen(QWidget):
    def __init__(self,menu_ref=None):
        super().__init__()
        self.menu_ref = menu_ref
        self.setStyleSheet("background-color: #0a0a0a;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top navbar 
        layout.addWidget(self.create_navbar())

        #  Scrollable content 
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(48, 32, 48, 48)
        content_layout.setSpacing(28)

        content_layout.addWidget(self.create_header())
        content_layout.addWidget(self.create_stats_row())
        content_layout.addWidget(self.create_heatmap_section())
        content_layout.addWidget(self.create_monthly_breakdown())
        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    # NAVBAR 
    def create_navbar(self):
        nav = QWidget()
        nav.setFixedHeight(56)
        nav.setStyleSheet("""
            background: #0a0a0a;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        """)
        h = QHBoxLayout(nav)
        h.setContentsMargins(24, 0, 24, 0)

        # App name
        app_name = QLabel("⚡ REPMARO")
        app_name.setStyleSheet("""
            color: #c8ff00;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 3px;
        """)

        # Back button
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

        # Page label
        page_lbl = QLabel("ACTIVITY RECORD")
        page_lbl.setStyleSheet("""
            color: #666680;
            font-size: 11px;
            letter-spacing: 3px;
        """)

        h.addWidget(app_name)
        h.addStretch()
        h.addWidget(page_lbl)
        h.addStretch()
        h.addWidget(back_btn)
        return nav

    #  HEADER 
    def create_header(self):
        widget = QWidget()
        h = QHBoxLayout(widget)
        h.setContentsMargins(0, 0, 0, 0)

        # Left
        left = QVBoxLayout()
        left.setSpacing(6)

        tag = QLabel("YOUR STATS")
        tag.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 3px;")

        title = QLabel("ACTIVITY\nRECORD")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 46px;
            font-weight: bold;
            line-height: 1;
        """)

        sub = QLabel("Every drop of sweat — tracked and counted")
        sub.setStyleSheet("color: #666680; font-size: 13px;")

        left.addWidget(tag)
        left.addWidget(title)
        left.addWidget(sub)
        h.addLayout(left)
        h.addStretch()

        # Right  Year tabs
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignBottom)
        tabs_lbl = QLabel("YEAR")
        tabs_lbl.setStyleSheet("color: #666680; font-size: 9px; letter-spacing: 2px;")
        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(8)

        for year in ["2023", "2024", "2025"]:
            btn = QPushButton(year)
            btn.setFixedSize(72, 34)
            btn.setCursor(Qt.PointingHandCursor)
            if year == "2025":
                btn.setStyleSheet("""
                    QPushButton {
                        background: #c8ff00;
                        color: #0a0a0a;
                        border-radius: 8px;
                        font-weight: bold;
                        font-size: 12px;
                        border: none;
                    }
                    QPushButton:hover { background: #a8d400; }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: #666680;
                        border-radius: 8px;
                        font-size: 12px;
                        border: 1px solid rgba(255,255,255,0.07);
                    }
                    QPushButton:hover {
                        color: #ffffff;
                        border-color: rgba(255,255,255,0.15);
                    }
                """)
            tabs_row.addWidget(btn)

        right.addWidget(tabs_lbl)
        right.addLayout(tabs_row)
        h.addLayout(right)
        return widget

    #  STATS ROW 
    def create_stats_row(self):
        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(16)

        try:
            with open(SESSION_FILE, "r") as f:
                total_session = f.read().strip()
        except:
            total_session = "0"

        try:
            with open(TIME_FILE, "r") as f:
                sec = int(f.read().strip())
                mins = sec // 60
                time_str = f"{mins} min"
        except:
            time_str = "0 min"

        try:
            exercise, maxex = self.get_max_reps()
            maxex_str = str(maxex)
            ex_str    = str(exercise)
        except:
            maxex_str = "0"
            ex_str    = "N/A"

        try:
            year_pct = str(self.get_year_percentage()) + "%"
        except:
            year_pct = "0%"

        stats = [
            ("🏆", total_session, "TOTAL SESSIONS",  "↑ Keep it up!",          "#c8ff00"),
            ("🔥", maxex_str,     "BEST SESSION",     f"In {ex_str}",            "#ff6b35"),
            ("📆", year_pct,      "CONSISTENCY",      "This year so far",        "#00e676"),
            ("⏱️", time_str,      "TOTAL TIME",       "All workouts combined",   "#47b8ff"),
        ]

        for icon, val, label, sub, accent in stats:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: #1e1e2a;
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 16px;
                }}
                QFrame:hover {{
                    border-color: {accent}44;
                    background: #22222e;
                }}
            """)

            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 18, 20, 18)
            cl.setSpacing(6)

            
            top = QHBoxLayout()
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 24px;")
            accent_dot = QFrame()
            accent_dot.setFixedSize(6, 6)
            accent_dot.setStyleSheet(f"background: {accent}; border-radius: 3px;")
            top.addWidget(icon_lbl)
            top.addStretch()
            top.addWidget(accent_dot)
            cl.addLayout(top)

            val_lbl = QLabel(str(val))
            val_lbl.setStyleSheet(f"""
                font-size: 34px;
                font-weight: bold;
                color: {accent};
            """)

            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 10px; color: #666680; letter-spacing: 1px;")

            sub_lbl = QLabel(sub)
            sub_lbl.setStyleSheet("font-size: 10px; color: #444458;")

            cl.addWidget(val_lbl)
            cl.addWidget(lbl)
            cl.addWidget(sub_lbl)
            row.addWidget(card)

        return container

    # HEATMAP 
    def create_heatmap_section(self):
        wrap = QFrame()
        wrap.setStyleSheet("""
            QFrame {
                background: #1e1e2a;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 20px;
            }
        """)
        layout = QVBoxLayout(wrap)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

    # Title row
        title_row = QHBoxLayout()
        title = QLabel(f"WORKOUT HEATMAP — {date.today().year}")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; letter-spacing: 2px;")

        legend = QHBoxLayout()
        legend.setSpacing(6)
        less = QLabel("Less")
        less.setStyleSheet("color: #666680; font-size: 10px;")
        legend.addWidget(less)
        for color in ["#1e1e2a","rgba(200,255,0,0.15)","rgba(200,255,0,0.35)","rgba(200,255,0,0.6)","#c8ff00"]:
            dot = QFrame()
            dot.setFixedSize(13, 13)
            dot.setStyleSheet(f"background: {color}; border-radius: 3px;")
            legend.addWidget(dot)
        more = QLabel("More")
        more.setStyleSheet("color: #666680; font-size: 10px;")
        legend.addWidget(more)

        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addLayout(legend)
        layout.addLayout(title_row)

    #  Info bar 
        self.heatmap_info = QLabel("Hover over a cell to see details")
        self.heatmap_info.setFixedHeight(28)
        self.heatmap_info.setStyleSheet("""
            color: #666680;
            font-size: 11px;
            padding: 4px 8px;
            background: rgba(255,255,255,0.03);
            border-radius: 6px;
        """)
        layout.addWidget(self.heatmap_info)

        # Month labels
        months_row = QHBoxLayout()
        months_row.setSpacing(0)
        months_row.setContentsMargins(32, 0, 0, 0)
        for m in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
            lbl = QLabel(m)
            lbl.setStyleSheet("color: #666680; font-size: 9px;")
            lbl.setAlignment(Qt.AlignCenter)
            months_row.addWidget(lbl)
        layout.addLayout(months_row)

        # Grid row
        grid_row = QHBoxLayout()
        grid_row.setSpacing(8)

        day_col = QVBoxLayout()
        day_col.setSpacing(0)
        day_col.setContentsMargins(0, 2, 0, 0)
        for d in ["Mon", "", "Wed", "", "Fri", "", "Sun"]:
            lbl = QLabel(d)
            lbl.setFixedHeight(18)
            lbl.setStyleSheet("color: #666680; font-size: 9px;")
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            day_col.addWidget(lbl)
        grid_row.addLayout(day_col)

        grid = QGridLayout()
        grid.setSpacing(3)
    
        today = date.today()
        start = date(today.year, 1, 1)
        workout_days = {}

    #  Load dates 
        try:
            with open(DATE_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            d = date.fromisoformat(line)
                            if d.year == today.year:
                                workout_days[d] = min(workout_days.get(d, 0) + 1, 4)
                        except ValueError:
                            pass
        except FileNotFoundError:
            pass

        colors = {
            0: "rgba(255,255,255,0.03)",
            1: "rgba(200,255,0,0.12)",
            2: "rgba(200,255,0,0.30)",
            3: "rgba(200,255,0,0.58)",
            4: "#c8ff00",
        }

        offset = start.weekday()

        for week in range(53):
            for day in range(7):
                idx = week * 7 + day - offset
                cur = start + timedelta(days=idx)
    
                cell = QFrame()
                cell.setFixedSize(13, 13)
                cell.setCursor(Qt.PointingHandCursor)
    
                if cur.year != today.year or cur > today:
                    cell.setStyleSheet("background: rgba(255,255,255,0.02); border-radius: 3px;")
                else:
                    level    = workout_days.get(cur, 0)
                    is_today = cur == today
    
                    border = "border: 1px solid #c8ff00;" if is_today else ""
                    cell.setStyleSheet(f"""
                        background: {colors[level]};
                        border-radius: 3px;
                        {border}
                    """)
    
                    #  Rich tooltip 
                    day_name   = cur.strftime("%A")
                    date_str   = cur.strftime("%d %B %Y")
                    if level > 0:
                        tip = f"📅 {day_name}, {date_str}\n✓ Worked out {level}x"
                    else:
                        tip = f"📅 {day_name}, {date_str}\n— Rest day"
                    cell.setToolTip(tip)
    
                    # Hover shows info in bar 
                    cell.enterEvent = lambda e, c=cur, l=level: self.heatmap_info.setText(
                        f"📅  {c.strftime('%A, %d %B %Y')}   |   "
                        + (f"✓  Worked out {l}x" if l > 0 else "—  Rest day")
                    )
                    cell.leaveEvent = lambda e: self.heatmap_info.setText(
                        "Hover over a cell to see details"
                    )
    
                    # Click shows popup 
                    cell.mousePressEvent = lambda e, c=cur, l=level: self.show_day_popup(c, l)
    
                grid.addWidget(cell, day, week)

        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        grid_row.addWidget(grid_widget)
        layout.addLayout(grid_row)
        return wrap


    def show_day_popup(self, workout_date, level):
        """Shows a popup with details about a specific day"""
        popup = QDialog(self)
        popup.setWindowTitle("Day Details")
        popup.setFixedSize(300, 200)
        popup.setStyleSheet("""
            QDialog {
                background: #1e1e2a;
            }
        """)

        layout = QVBoxLayout(popup)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Date
        date_lbl = QLabel(workout_date.strftime("%A").upper())
        date_lbl.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 2px;")

        full_date = QLabel(workout_date.strftime("%d %B %Y"))
        full_date.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: bold;")
    
        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: rgba(255,255,255,0.07);")

        # Status
        if level > 0:
            status = QLabel(f"✓  Worked out {level}x this day")
            status.setStyleSheet("""
                color: #c8ff00;
                font-size: 14px;
                font-weight: bold;
                background: rgba(200,255,0,0.08);
                border: 1px solid rgba(200,255,0,0.2);
                border-radius: 8px;
                padding: 10px;
            """)
        else:
            status = QLabel("— Rest day")
            status.setStyleSheet("""
                color: #666680;
                font-size: 14px;
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 8px;
                padding: 10px;
            """)
        status.setAlignment(Qt.AlignCenter)

        # Close btn
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                color: #666680;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover { color: #ffffff; background: rgba(255,255,255,0.1); }
        """)
        close_btn.clicked.connect(popup.accept)
    
        layout.addWidget(date_lbl)
        layout.addWidget(full_date)
        layout.addWidget(div)
        layout.addWidget(status)
        layout.addWidget(close_btn)

        popup.exec_()

    #  MONTHLY BREAKDOWN 
    def create_monthly_breakdown(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # Title row
        title_row = QHBoxLayout()
        title = QLabel("MONTHLY BREAKDOWN")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
            letter-spacing: 2px;
        """)
        current_month_name = date.today().strftime("%B").upper()
        cur_lbl = QLabel(f"Current month: {current_month_name}")
        cur_lbl.setStyleSheet("""
            color: #c8ff00;
            font-size: 11px;
            background: rgba(200,255,0,0.08);
            border: 1px solid rgba(200,255,0,0.2);
            border-radius: 8px;
            padding: 4px 12px;
        """)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(cur_lbl)
        layout.addLayout(title_row)

        grid = QGridLayout()
        grid.setSpacing(12)

        months   = ["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"]
        days_in  = [31,28,31,30,31,30,31,31,30,31,30,31]
        cur_month = date.today().month - 1

        try:
            month_counts = self.get_month_counts()
        except:
            month_counts = [0] * 12

        for i, (month, total) in enumerate(zip(months, days_in)):
            count     = month_counts[i] if i <= cur_month else 0
            pct       = int((count / total) * 100) if i <= cur_month and total > 0 else 0
            is_future = i > cur_month
            is_cur    = i == cur_month

            card = QFrame()
            if is_cur:
                border = "#c8ff00"
            elif is_future:
                border = "rgba(255,255,255,0.04)"
            else:
                border = "rgba(255,255,255,0.07)"

            card.setStyleSheet(f"""
                QFrame {{
                    background: {'#1e1e2a' if not is_future else '#141414'};
                    border: 1px solid {border};
                    border-radius: 12px;
                }}
            """)
            if is_future:
                eff = QGraphicsOpacityEffect()
                eff.setOpacity(0.3)
                card.setGraphicsEffect(eff)

            cl = QVBoxLayout(card)
            cl.setContentsMargins(14, 12, 14, 12)
            cl.setSpacing(5)

            
            top = QHBoxLayout()
            name_lbl = QLabel(month.upper())
            name_lbl.setStyleSheet("color: #666680; font-size: 10px; letter-spacing: 1px; font-weight: bold;")
            top.addWidget(name_lbl)
            if is_cur:
                now = QLabel("NOW")
                now.setStyleSheet("""
                    color: #0a0a0a;
                    background: #c8ff00;
                    font-size: 7px;
                    font-weight: bold;
                    border-radius: 4px;
                    padding: 1px 5px;
                """)
                top.addWidget(now)
            top.addStretch()
            cl.addLayout(top)

            days_lbl = QLabel(f"{count}/{total}" if not is_future else "—")
            days_lbl.setStyleSheet(f"""
                font-size: 20px;
                font-weight: bold;
                color: {'#c8ff00' if is_cur else '#ffffff' if not is_future else '#444458'};
            """)

            bar_bg = QFrame()
            bar_bg.setFixedHeight(4)
            bar_bg.setStyleSheet("background: rgba(255,255,255,0.06); border-radius: 2px;")
            bar_fill = QFrame(bar_bg)
            bar_fill.setFixedHeight(4)
            bar_fill.setStyleSheet("""
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #00e676, stop:1 #c8ff00);
                border-radius: 2px;
            """)
            bar_fill.setFixedWidth(int((pct / 100) * 100))

            pct_lbl = QLabel(f"{pct}%" if not is_future else "—")
            pct_lbl.setStyleSheet("font-size: 10px; color: #666680;")

            cl.addWidget(days_lbl)
            cl.addWidget(bar_bg)
            cl.addWidget(pct_lbl)

            grid.addWidget(card, i // 6, i % 6)

        layout.addLayout(grid)
        return widget

    def get_max_reps(self):
        max_reps, max_exercise = 0, ""
        with open(REPS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    reps     = int(parts[-1])
                    exercise = " ".join(parts[:-1])
                    if reps > max_reps:
                        max_reps     = reps
                        max_exercise = exercise
        return max_exercise, max_reps

    def load_workout_dates(self):
        dates = []
        with open(DATE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    dates.append(date.fromisoformat(line))
        return dates

    def get_month_counts(self):
        month_counts = [0] * 12
        for d in self.load_workout_dates():
            month_counts[d.month - 1] += 1
        return month_counts

    def get_year_percentage(self):
        today      = date.today()
        start      = date(today.year, 1, 1)
        workout_days = 0
        with open(DATE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    d = date.fromisoformat(line)
                    if d.year == today.year:
                        workout_days += 1
        days_passed = (today - start).days + 1
        return int((workout_days / days_passed) * 100)

    def go_back_to_menu(self):
        if self.menu_ref:
            if self.window().isMaximized():
                self.menu_ref.showMaximized()
            else:
                self.menu_ref.resize(self.window().width(), self.window().height())
                self.menu_ref.show()
            self.window().close()
        else:
            from menur import MainWindow
            self.menu = MainWindow()
            self.menu.show()
            self.window().close()
    def resizeEvent(self, event):
       self.current_size = (self.width(), self.height())
       super().resizeEvent(event)  

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background: #0a0a0a; color: #ffffff; font-family: 'Segoe UI'; }")
    w = QMainWindow()
    w.resize(1280, 720)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("border: none; background: #0a0a0a;")
    scroll.setWidget(RecordScreen())
    w.setCentralWidget(scroll)
    w.show()
    sys.exit(app.exec_())