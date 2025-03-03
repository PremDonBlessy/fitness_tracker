import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.signup import SignupScreen
from ui.dashboard import DashboardScreen
from database.db_config import get_db_connection

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.password_input = None
        self.username_input = None
        self.signup_window = None
        self.dashboard_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f0f0f0;")

        title_label = QLabel("🔑 Login to Fitness Tracker")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 12))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")

        login_button = QPushButton("Login")
        login_button.setFont(QFont("Arial", 12))
        login_button.setStyleSheet("background-color: #4CAF50; color: white;")
        login_button.clicked.connect(self.login_user)

        signup_button = QPushButton("Sign Up")
        signup_button.setFont(QFont("Arial", 12))
        signup_button.setStyleSheet("background-color: #2196F3; color: white;")
        signup_button.clicked.connect(self.open_signup)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = SHA2(%s, 256)", (username, password))
            user = cursor.fetchone()

            if user:
                QMessageBox.information(self, "Success", "Login successful! 🚀")
                self.dashboard_window = DashboardScreen()
                self.dashboard_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")

    def open_signup(self):
        self.signup_window = SignupScreen()
        self.signup_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginScreen()
    login_window.show()
    sys.exit(app.exec_())
