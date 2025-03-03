from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QDateEdit, QComboBox, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QDate

# ✅ Import Database Properly
try:
    from database.db_config import Database  # Ensure correct import
    db = Database()
except Exception as e:
    print(f"Database Connection Error: {e}")
    db = None  # Prevent crashes

class RemindersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Reminders")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        # Reminder List Label
        self.reminder_list_label = QLabel("Reminder List")
        layout.addWidget(self.reminder_list_label)

        # Reminder Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Client ID", "Reminder Date", "Message", "Status"])
        layout.addWidget(self.table)

        # Buttons for Add, Edit, Delete
        button_layout = QHBoxLayout()

        self.btn_add = QPushButton("Add Reminder")
        self.btn_add.clicked.connect(self.clear_form)
        button_layout.addWidget(self.btn_add)

        self.btn_edit = QPushButton("Edit Reminder")
        self.btn_edit.clicked.connect(self.edit_reminder)
        button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("Delete Reminder")
        self.btn_delete.clicked.connect(self.delete_reminder)
        button_layout.addWidget(self.btn_delete)

        layout.addLayout(button_layout)

        # Reminder Form Inputs
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID")
        layout.addWidget(self.client_id_input)

        self.reminder_date = QDateEdit()
        self.reminder_date.setCalendarPopup(True)
        self.reminder_date.setDate(QDate.currentDate())
        layout.addWidget(self.reminder_date)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message")
        layout.addWidget(self.message_input)

        self.status_dropdown = QComboBox()
        self.status_dropdown.addItems(["Pending", "Done", "Overdue"])
        layout.addWidget(self.status_dropdown)

        # Save and Cancel Buttons
        action_layout = QHBoxLayout()

        self.btn_save = QPushButton("Save Reminder")
        self.btn_save.clicked.connect(self.save_reminder)
        action_layout.addWidget(self.btn_save)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.clear_form)
        action_layout.addWidget(self.btn_cancel)

        layout.addLayout(action_layout)

        self.setLayout(layout)

        self.load_reminders()  # ✅ Load reminders on startup

    def load_reminders(self):
        """Fetch and display all reminders from the database."""
        if db is None:
            QMessageBox.critical(self, "Database Error", "Database connection is not available.")
            return

        try:
            reminders = db.get_reminders()
            self.table.setRowCount(len(reminders))

            for row, data in enumerate(reminders):
                self.table.setItem(row, 0, QTableWidgetItem(str(data["client_id"])))
                self.table.setItem(row, 1, QTableWidgetItem(data["reminder_date"]))
                self.table.setItem(row, 2, QTableWidgetItem(data["message"]))
                self.table.setItem(row, 3, QTableWidgetItem(data["status"]))

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load reminders: {e}")

    def save_reminder(self):
        """Save a new or edited reminder."""
        if db is None:
            QMessageBox.critical(self, "Database Error", "Database connection is not available.")
            return

        client_id = self.client_id_input.text().strip()
        reminder_date = self.reminder_date.date().toString("yyyy-MM-dd")
        message = self.message_input.text().strip()
        status = self.status_dropdown.currentText()

        if not client_id or not message:
            QMessageBox.warning(self, "Input Error", "Please enter a Client ID and Message.")
            return

        try:
            db.save_reminder(client_id, reminder_date, message, status)
            self.load_reminders()  # Refresh UI
            QMessageBox.information(self, "Success", "Reminder saved successfully!")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save reminder: {e}")

    def edit_reminder(self):
        """Load selected reminder into input fields."""
        selected = self.table.currentRow()
        if selected >= 0:
            self.client_id_input.setText(self.table.item(selected, 0).text())
            self.reminder_date.setDate(QDate.fromString(self.table.item(selected, 1).text(), "yyyy-MM-dd"))
            self.message_input.setText(self.table.item(selected, 2).text())
            self.status_dropdown.setCurrentText(self.table.item(selected, 3).text())

    def delete_reminder(self):
        """Delete selected reminder."""
        if db is None:
            QMessageBox.critical(self, "Database Error", "Database connection is not available.")
            return

        selected = self.table.currentRow()
        if selected >= 0:
            client_id = self.table.item(selected, 0).text()
            reminder_date = self.table.item(selected, 1).text()

            confirm = QMessageBox.question(self, "Confirm Deletion",
                                           f"Are you sure you want to delete this reminder?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    db.delete_reminder(client_id, reminder_date)
                    self.load_reminders()  # Refresh UI
                    QMessageBox.information(self, "Success", "Reminder deleted successfully!")

                except Exception as e:
                    QMessageBox.critical(self, "Database Error", f"Failed to delete reminder: {e}")

    def clear_form(self):
        """Clear input fields for adding a new reminder."""
        self.client_id_input.clear()
        self.message_input.clear()
        self.status_dropdown.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    window = RemindersWindow()
    window.show()
    app.exec_()
