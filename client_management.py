import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

CLIENTS_FILE = "clients.json"

class ClientManagementScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.clients = {}
        self.load_clients()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Client Management")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #F5F5F5;")

        title_label = QLabel("🏋️‍♂️ Client Management (Add/Edit/Delete Clients)")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #1A237E;")

        self.client_list = QListWidget()
        self.client_list.setFixedHeight(150)

        show_all_btn = QPushButton("🔍 Show All Clients")
        show_all_btn.clicked.connect(self.show_all_clients)

        form_label = QLabel("📌 Client Details Form")
        form_label.setFont(QFont("Arial", 14, QFont.Bold))
        form_label.setStyleSheet("color: #0D47A1;")

        self.client_id = QLineEdit()
        self.client_name = QLineEdit()
        self.client_age = QLineEdit()
        self.client_weight = QLineEdit()
        self.client_goal = QLineEdit()

        self.client_id.setPlaceholderText("Enter Client ID")
        self.client_name.setPlaceholderText("Enter Client Name")
        self.client_age.setPlaceholderText("Enter Age")
        self.client_weight.setPlaceholderText("Enter Weight")
        self.client_goal.setPlaceholderText("Enter Fitness Goal")

        add_client_btn = QPushButton("➕ Add Client")
        edit_client_btn = QPushButton("✏️ Edit Client")
        delete_client_btn = QPushButton("🗑️ Delete Client")
        save_btn = QPushButton("💾 Save")
        cancel_btn = QPushButton("❌ Cancel")

        add_client_btn.clicked.connect(self.add_client)
        edit_client_btn.clicked.connect(self.edit_client)
        delete_client_btn.clicked.connect(self.delete_client)
        save_btn.clicked.connect(self.save_client_data)
        cancel_btn.clicked.connect(self.clear_form)

        top_layout = QVBoxLayout()
        top_layout.addWidget(title_label)
        top_layout.addWidget(self.client_list)
        top_layout.addWidget(show_all_btn)

        form_layout = QVBoxLayout()
        form_layout.addWidget(form_label)
        form_layout.addWidget(self.client_id)
        form_layout.addWidget(self.client_name)
        form_layout.addWidget(self.client_age)
        form_layout.addWidget(self.client_weight)
        form_layout.addWidget(self.client_goal)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_client_btn)
        button_layout.addWidget(edit_client_btn)
        button_layout.addWidget(delete_client_btn)

        save_cancel_layout = QHBoxLayout()
        save_cancel_layout.addWidget(save_btn)
        save_cancel_layout.addWidget(cancel_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(save_cancel_layout)
        main_layout.setSpacing(10)

        self.setLayout(main_layout)
        self.show_all_clients()

    def load_clients(self):
        try:
            with open(CLIENTS_FILE, "r") as file:
                self.clients = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.clients = {}

    def save_clients_to_file(self):
        with open(CLIENTS_FILE, "w") as file:
            json.dump(self.clients, file, indent=4)

    def show_all_clients(self):
        self.client_list.clear()
        for client_id, details in self.clients.items():
            self.client_list.addItem(f"ID: {client_id}, Name: {details['name']}, Age: {details['age']}")

    def add_client(self):
        client_id = self.client_id.text().strip()
        name = self.client_name.text().strip()
        age = self.client_age.text().strip()
        weight = self.client_weight.text().strip()
        goal = self.client_goal.text().strip()

        if not client_id or not name or not age or not weight or not goal:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        if client_id in self.clients:
            QMessageBox.warning(self, "Duplicate Error", "Client ID already exists!")
            return

        self.clients[client_id] = {
            "name": name, "age": age, "weight": weight, "goal": goal
        }
        self.save_clients_to_file()
        self.show_all_clients()
        self.clear_form()
        QMessageBox.information(self, "Success", "Client Added Successfully!")

    def edit_client(self):
        selected_item = self.client_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Select a client to edit!")
            return

        client_id = selected_item.text().split(",")[0].split(":")[1].strip()
        client_data = self.clients[client_id]

        self.client_id.setText(client_id)
        self.client_name.setText(client_data["name"])
        self.client_age.setText(client_data["age"])
        self.client_weight.setText(client_data["weight"])
        self.client_goal.setText(client_data["goal"])

    def delete_client(self):
        selected_item = self.client_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Select a client to delete!")
            return

        client_id = selected_item.text().split(",")[0].split(":")[1].strip()

        confirmation = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete {self.clients[client_id]['name']}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            del self.clients[client_id]
            self.save_clients_to_file()
            self.show_all_clients()
            QMessageBox.information(self, "Success", "Client Deleted Successfully!")

    def save_client_data(self):
        client_id = self.client_id.text().strip()
        if client_id not in self.clients:
            QMessageBox.warning(self, "Save Error", "Client does not exist!")
            return

        self.clients[client_id] = {
            "name": self.client_name.text().strip(),
            "age": self.client_age.text().strip(),
            "weight": self.client_weight.text().strip(),
            "goal": self.client_goal.text().strip()
        }
        self.save_clients_to_file()
        self.show_all_clients()
        self.clear_form()
        QMessageBox.information(self, "Success", "Client Data Updated Successfully!")

    def clear_form(self):
        self.client_id.clear()
        self.client_name.clear()
        self.client_age.clear()
        self.client_weight.clear()
        self.client_goal.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_mgmt = ClientManagementScreen()
    client_mgmt.show()
    sys.exit(app.exec_())
