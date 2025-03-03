from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
from database.database import Database  # ✅ Corrected import

class ChartsWindow(QWidget):
    def __init__(self):
        super().__init__()

        print("✅ ChartsWindow Initialized")  # Debugging print

        self.setWindowTitle("Client Progress Charts")
        self.setGeometry(100, 100, 600, 400)

        try:
            self.db = Database()  # ✅ Try connecting to the database
            print("✅ Database connected successfully!")  # Debugging print
        except Exception as e:
            print(f"❌ Database connection failed: {e}")  # Debugging print
            return  # Stop execution if DB connection fails

        layout = QVBoxLayout()

        # Dropdown to select Client ID
        self.client_id_label = QLabel("Select Client ID:")
        layout.addWidget(self.client_id_label)

        self.client_id_dropdown = QComboBox()
        layout.addWidget(self.client_id_dropdown)

        # Load Client IDs
        self.load_client_ids()

        self.client_id_dropdown.currentIndexChanged.connect(self.load_chart_data)

        # Chart display
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        # Table display
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Date", "Weight (Kgs)"])
        layout.addWidget(self.table)

        # Buttons
        self.btn_save_chart = QPushButton("Save Chart")
        layout.addWidget(self.btn_save_chart)

        self.btn_back = QPushButton("Back to Dashboard")
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def load_client_ids(self):
        """Load client IDs into dropdown."""
        try:
            clients = self.db.get_all_clients()
            if not clients:
                print("⚠️ No clients found in the database.")  # Debugging print
                return

            for client in clients:
                self.client_id_dropdown.addItem(f"{client['id']} - {client['name']}", client['id'])

            print("✅ Clients loaded successfully")  # Debugging print
        except Exception as e:
            print(f"❌ Error loading clients: {e}")

    def load_chart_data(self):
        """Fetch progress data for the selected client and update the chart."""
        client_id = self.client_id_dropdown.currentData()
        if not client_id:
            print("⚠️ No client selected.")  # Debugging print
            return

        print(f"📊 Loading progress data for Client ID: {client_id}")  # Debugging print

        progress_data = self.db.get_progress(client_id)

        if not progress_data:
            print("⚠️ No progress data found for this client.")  # Debugging print
            return

        # Update Table
        self.table.setRowCount(len(progress_data))
        for row, data in enumerate(progress_data):
            self.table.setItem(row, 0, QTableWidgetItem(data["date"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(data["weight"])))

        # Update Chart
        self.update_chart(progress_data)

    def update_chart(self, progress_data):
        """Plot weight progress over time."""
        series = QLineSeries()
        for data in progress_data:
            date = QDateTime.fromString(data["date"], "yyyy-MM-dd").toMSecsSinceEpoch()
            series.append(date, data["weight"])

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Weight Progress Over Time")

        # X-Axis (Date)
        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd/MM/yyyy")
        axis_x.setTitleText("Date")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Y-Axis (Weight)
        axis_y = QValueAxis()
        axis_y.setTitleText("Weight (Kgs)")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart_view.setChart(chart)
        print("✅ Chart updated successfully!")  # Debugging print

if __name__ == "__main__":
    app = QApplication([])
    window = ChartsWindow()
    window.show()
    app.exec_()
