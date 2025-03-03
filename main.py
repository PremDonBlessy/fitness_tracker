import sys
from PyQt5.QtWidgets import QApplication
from ui.login import LoginScreen  # Import LoginScreen

def main():
    app = QApplication(sys.argv)

    # Initialize and display the login screen
    login_window = LoginScreen()
    login_window.show()

    sys.exit(app.exec_())  # Start event loop

if __name__ == "__main__":
    main()
