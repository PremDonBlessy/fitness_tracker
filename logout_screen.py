from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
import sys

class LogoutScreen(QWidget):
    def __init__(self, login_screen_callback):
        super().__init__()
        self.setWindowTitle("Logout Confirmation")
        self.setGeometry(300, 200, 700, 500)  # Even Bigger Window

        self.login_screen_callback = login_screen_callback  # Callback to return to login screen

        # Apply Dark Theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
            }
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 30px;
            }
            QPushButton {
                font-size: 24px;
                padding: 25px;
                border-radius: 12px;
                min-width: 300px;
            }
            QPushButton#logoutBtn {
                background-color: #D32F2F;
                color: white;
            }
            QPushButton#logoutBtn:hover {
                background-color: #FF5252;
            }
            QPushButton#cancelBtn {
                background-color: #555;
                color: white;
            }
            QPushButton#cancelBtn:hover {
                background-color: #777;
            }
        """)

        # Logout Message
        self.message_label = QLabel("Are you sure you want to logout and return to the login screen?", self)
        self.message_label.setFont(QFont("Arial", 26))
        self.message_label.setWordWrap(True)

        # Buttons
        self.logout_button = QPushButton("✅ YES, LOGOUT", self)
        self.logout_button.setObjectName("logoutBtn")
        self.logout_button.clicked.connect(self.logout)

        self.cancel_button = QPushButton("❌ CANCEL", self)
        self.cancel_button.setObjectName("cancelBtn")
        self.cancel_button.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.cancel_button)
        layout.setSpacing(30)  # Increased Spacing
        self.setLayout(layout)

    def logout(self):
        """Logout and return to the login screen."""
        self.close()  # Close logout screen
        self.login_screen_callback()  # Redirect to login screen

if __name__ == "__main__":
    def dummy_login_screen():
        print("Redirecting to Login Screen...")  # Replace with actual login screen logic

    app = QApplication(sys.argv)
    window = LogoutScreen(dummy_login_screen)
    window.show()
    sys.exit(app.exec_())
