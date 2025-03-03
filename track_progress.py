import sys
import pandas as pd
from fpdf import FPDF
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import QDate, Qt
import matplotlib.pyplot as plt

# ✅ Import Database Correctly
try:
    from database.db_config import Database

    db = Database()
except Exception as e:
    print(f"Database Import Error: {e}")
    db = None  # Prevents crashing


class TrackProgressUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track Client Progress")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        self.client_id_dropdown = QComboBox()
        self.client_id_dropdown.currentIndexChanged.connect(self.load_client_name)

        self.client_name_field = QLineEdit()
        self.client_name_field.setReadOnly(True)

        self.date_field = QLineEdit(QDate.currentDate().toString(Qt.ISODate))
        self.weight_field = QLineEdit()
        self.notes_field = QTextEdit()

        self.add_btn = QPushButton("Add Progress")
        self.add_btn.clicked.connect(self.add_progress)

        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(3)
        self.progress_table.setHorizontalHeaderLabels(["Date", "Weight (kg)", "Notes"])

        layout.addWidget(QLabel("Select Client ID:"))
        layout.addWidget(self.client_id_dropdown)
        layout.addWidget(QLabel("Client Name:"))
        layout.addWidget(self.client_name_field)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_field)
        layout.addWidget(QLabel("Weight (kg):"))
        layout.addWidget(self.weight_field)
        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_field)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.progress_table)

        self.setLayout(layout)

        # ✅ Always Open the UI
        self.load_clients()

    def load_clients(self):
        """Load clients into dropdown."""
        if db is None:
            print("Error: Database connection failed.")
            return

        try:
            self.client_id_dropdown.clear()
            clients = db.get_all_clients()

            if not clients:
                QMessageBox.warning(self, "Warning", "No clients found in the database!")

            for client in clients:
                self.client_id_dropdown.addItem(f"{client['id']} - {client['name']}", client['id'])

        except Exception as e:
            print(f"Error loading clients: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to load clients: {e}")

    def load_client_name(self):
        """Auto-fill client name."""
        if db is None:
            return

        client_id = self.client_id_dropdown.itemData(self.client_id_dropdown.currentIndex())
        if client_id:
            self.client_name_field.setText(db.get_client_name(client_id))

    def add_progress(self):
        """Add new progress entry."""
        if db is None:
            QMessageBox.critical(self, "Error", "Database connection is not available.")
            return

        client_id = self.client_id_dropdown.itemData(self.client_id_dropdown.currentIndex())
        date = self.date_field.text()
        weight = self.weight_field.text()
        notes = self.notes_field.toPlainText()

        if client_id and date and weight:
            try:
                db.add_progress(client_id, date, weight, notes)
                self.load_progress(client_id)
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to add progress: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrackProgressUI()
    window.show()
    sys.exit(app.exec_())
