import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.client_management import ClientManagementScreen
from ui.track_progress import TrackProgressUI
from ui.reports import ReportsWindow
from ui.charts import ChartsWindow
from ui.reminders import RemindersWindow
from ui.activity_tracking import ActivityTrackingWindow

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Fitness Tracker Dashboard")
        self.setGeometry(100, 100, 1024, 600)

        title_label = QLabel("🏋️‍♂️ Welcome to Fitness Tracker Management System")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        self.buttons = {
            "Client Management": QPushButton("👤 Client Management"),
            "Track Progress": QPushButton("📊 Track Progress"),
            "Reports": QPushButton("📑 Reports"),
            "View Charts": QPushButton("📈 View Charts"),
            "Set Reminders": QPushButton("⏰ Set Reminders"),
            "Activity Tracker": QPushButton("🔥 Activity Tracker"),
            "Logout": QPushButton("🚪 Log Out")
        }

        for btn in self.buttons.values():
            btn.setFont(QFont("Arial", 14))
            btn.setFixedHeight(50)

        top_row = QHBoxLayout()
        top_row.addWidget(self.buttons["Client Management"])
        top_row.addWidget(self.buttons["Track Progress"])
        top_row.addWidget(self.buttons["Reports"])

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(self.buttons["View Charts"])
        bottom_row.addWidget(self.buttons["Set Reminders"])
        bottom_row.addWidget(self.buttons["Activity Tracker"])

        logout_layout = QVBoxLayout()
        logout_layout.addWidget(self.buttons["Logout"], alignment=Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_row)
        main_layout.addLayout(bottom_row)
        main_layout.addLayout(logout_layout)

        self.setLayout(main_layout)

        self.buttons["Client Management"].clicked.connect(self.open_client_management)
        self.buttons["Track Progress"].clicked.connect(self.open_track_progress)
        self.buttons["Reports"].clicked.connect(self.open_reports)
        self.buttons["View Charts"].clicked.connect(self.open_charts)
        self.buttons["Set Reminders"].clicked.connect(self.open_reminders)
        self.buttons["Activity Tracker"].clicked.connect(self.open_activity_tracker)
        self.buttons["Logout"].clicked.connect(self.logout)

    def open_client_management(self):
        self.client_management_window = ClientManagementScreen()
        self.client_management_window.show()

    def open_track_progress(self):
        try:
            self.track_progress_window = TrackProgressUI()
            self.track_progress_window.show()
        except Exception as e:
            print(f"Error opening Track Progress: {e}")

    def open_reports(self):
        self.reports_window = ReportsWindow()
        self.reports_window.show()

    def open_charts(self):
        self.charts_window = ChartsWindow()
        self.charts_window.show()

    def open_reminders(self):
        self.reminders_window = RemindersWindow()
        self.reminders_window.show()

    def open_activity_tracker(self):
        self.activity_window = ActivityTrackingWindow()
        self.activity_window.show()

    def logout(self):
        from ui.login import LoginScreen
        self.login_screen = LoginScreen()
        self.login_screen.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = DashboardScreen()
    dashboard.show()
    sys.exit(app.exec_())
