# ui/forgot_password.py

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

class ForgotPasswordScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.confirm_input = None
        self.new_password_input = None
        self.username_input = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Forgot Password")
        self.setGeometry(200, 200, 400, 250)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Title Label
        title_label = QLabel("Reset Password")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))

        # Username Input
        username_label = QLabel("Enter Username:")
        username_label.setFont(QFont("Arial", 12))
        self.username_input = QLineEdit()

        # New Password Input
        new_password_label = QLabel("New Password:")
        new_password_label.setFont(QFont("Arial", 12))
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)

        # Confirm Password Input
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setFont(QFont("Arial", 12))
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)

        # Reset Button
        reset_button = QPushButton("Reset Password")
        reset_button.setFont(QFont("Arial", 12))
        reset_button.setStyleSheet("background-color: #FF5722; color: white; padding: 10px;")
        reset_button.clicked.connect(self.reset_password)

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
        layout.addWidget(new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(reset_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def reset_password(self):
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_input.text().strip()

        if not username or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the user exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user:
                QMessageBox.warning(self, "Error", "Username not found.")
            else:
                # Update password with SHA-256 hash
                cursor.execute("UPDATE users SET password = SHA2(%s, 256) WHERE username = %s", (new_password, username))
                conn.commit()
                QMessageBox.information(self, "Success", "Password reset successfully! You can now log in.")
                self.close()

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    forgot_window = ForgotPasswordScreen()
    forgot_window.show()
    sys.exit(app.exec_())
