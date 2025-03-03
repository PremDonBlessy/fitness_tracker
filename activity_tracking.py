from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QSpinBox
from database.database import Database

class ActivityTrackingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Activity and Calorie Tracking")
        self.setGeometry(200, 200, 700, 500)

        # ✅ TRY TO CONNECT TO DATABASE SAFELY
        try:
            self.db = Database()
            print("✅ Database connection established")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return  # Prevent UI from loading if database connection fails

        # CLIENT SELECTION
        self.client_dropdown = QComboBox()
        self.load_clients()

        # ACTIVITY SELECTION
        self.activity_dropdown = QComboBox()
        self.activity_list = self.load_activity_list()
        self.activity_dropdown.addItems(self.activity_list.keys())

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 300)  # 1 to 300 minutes

        self.calculate_button = QPushButton("Calculate Calories")
        self.calculate_button.clicked.connect(self.calculate_calories)

        self.log_button = QPushButton("Log Activity")
        self.log_button.clicked.connect(self.log_activity)

        self.calories_label = QLabel("Calories Burned: 0")

        # ACTIVITY LOG TABLE
        self.activity_table = QTableWidget(0, 3)
        self.activity_table.setHorizontalHeaderLabels(["Activity", "Duration", "Calories Burned"])

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Client:"))
        layout.addWidget(self.client_dropdown)
        layout.addWidget(QLabel("Select Activity:"))
        layout.addWidget(self.activity_dropdown)
        layout.addWidget(QLabel("Duration (minutes):"))
        layout.addWidget(self.duration_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.calories_label)
        layout.addWidget(self.log_button)
        layout.addWidget(QLabel("Today's Activity Log:"))
        layout.addWidget(self.activity_table)

        self.setLayout(layout)

    def load_clients(self):
        """Load clients from the database into dropdown."""
        try:
            clients = self.db.get_all_clients()
            if not clients:
                print("⚠️ No clients found in the database")
                return
            for client in clients:
                self.client_dropdown.addItem(f"{client['id']} - {client['name']}", client['id'])
            print("✅ Clients loaded successfully")
        except Exception as e:
            print(f"❌ Error loading clients: {e}")

    def load_activity_list(self):
        """Load available activities from the database."""
        try:
            activity_list = self.db.get_activity_list()
            if not activity_list:
                print("⚠️ No activities found")
                return {}
            print("✅ Activities loaded successfully")
            return activity_list
        except Exception as e:
            print(f"❌ Error loading activities: {e}")
            return {}

    def calculate_calories(self):
        """Calculate calories burned based on activity and duration."""
        activity = self.activity_dropdown.currentText()
        duration = self.duration_input.value()
        calories = self.activity_list.get(activity, 0) * duration
        self.calories_label.setText(f"Calories Burned: {calories}")

    def log_activity(self):
        """Log activity in the database."""
        client_id = self.client_dropdown.currentData()
        activity = self.activity_dropdown.currentText()
        duration = self.duration_input.value()
        calories = self.activity_list.get(activity, 0) * duration

        if client_id:
            try:
                self.db.log_activity(client_id, activity, duration, calories)
                print(f"✅ Activity logged: {activity}, {duration} mins, {calories} kcal")
                self.load_activity_log()
            except Exception as e:
                print(f"❌ Error logging activity: {e}")

    def load_activity_log(self):
        """Load today's activity log for the selected client."""
        client_id = self.client_dropdown.currentData()
        try:
            logs = self.db.get_today_activity_log(client_id)
            if not logs:
                print("⚠️ No activity logs found for today.")
                self.activity_table.setRowCount(0)
                return

            self.activity_table.setRowCount(len(logs))
            for row, data in enumerate(logs):
                self.activity_table.setItem(row, 0, QTableWidgetItem(data["activity"]))
                self.activity_table.setItem(row, 1, QTableWidgetItem(str(data["duration"])))
                self.activity_table.setItem(row, 2, QTableWidgetItem(str(data["calories_burned"])))

            print("✅ Activity log loaded")
        except Exception as e:
            print(f"❌ Error loading activity log: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = ActivityTrackingWindow()
    window.show()
    app.exec_()
