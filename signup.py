# ui/signup.py

import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change if needed
        password="Welcome@123456",  # Change if needed
        database="fitness_tracker"
    )

class SignupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.confirm_input = None
        self.password_input = None
        self.username_input = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sign Up")
        self.setGeometry(150, 150, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Title Label
        title_label = QLabel("Sign Up")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))

        # Username Input
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 12))
        self.username_input = QLineEdit()

        # Password Input
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Confirm Password Input
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setFont(QFont("Arial", 12))
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)

        # Sign Up Button
        signup_button = QPushButton("Sign Up")
        signup_button.setFont(QFont("Arial", 12))
        signup_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        signup_button.clicked.connect(self.signup_user)

        # Back to Login Button
        back_button = QPushButton("Back to Login")
        back_button.setFont(QFont("Arial", 12))
        back_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        back_button.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(signup_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def signup_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_input.text().strip()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                QMessageBox.warning(self, "Error", "Username already exists.")
            else:
                # Insert new user with SHA-256 hashed password
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, SHA2(%s, 256))", (username, password))
                conn.commit()
                QMessageBox.information(self, "Success", "Account created successfully! You can now log in.")
                self.close()

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    signup_window = SignupScreen()
    signup_window.show()
    sys.exit(app.exec_())
