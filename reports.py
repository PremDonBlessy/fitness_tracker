from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QRadioButton,
    QDateEdit, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from fpdf import FPDF

# ✅ Import Database Properly
try:
    from database.db_config import database

    db = Database()

except Exception as e:
    print(f"Database Connection Error: {e}")
    db = None  # Prevents crashes

class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Reports")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        # Report Type Selection
        self.report_type_label = QLabel("Report Type:")
        layout.addWidget(self.report_type_label)

        self.monthly_report = QRadioButton("Monthly Progress Report")
        self.seasonal_report = QRadioButton("Seasonal Progress Report")
        self.client_report = QRadioButton("Client Specific Report")

        layout.addWidget(self.monthly_report)
        layout.addWidget(self.seasonal_report)
        layout.addWidget(self.client_report)

        # Generate Report Button
        self.btn_generate_report = QPushButton("Generate Report")
        self.btn_generate_report.clicked.connect(self.load_report_data)
        layout.addWidget(self.btn_generate_report)

        # Report Filters
        self.filter_label = QLabel("Report Filters")
        layout.addWidget(self.filter_label)

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID")
        layout.addWidget(self.client_id_input)

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Client Name")
        layout.addWidget(self.client_name_input)

        # Start Date and End Date
        date_layout = QHBoxLayout()

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date)

        layout.addLayout(date_layout)

        # Table Display
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Date", "Weight (Kgs)", "Notes"])
        layout.addWidget(self.table)

        # Export to PDF Button
        self.btn_export_pdf = QPushButton("Export to PDF")
        self.btn_export_pdf.clicked.connect(self.export_to_pdf)
        layout.addWidget(self.btn_export_pdf)

        self.setLayout(layout)

    def load_report_data(self):
        """Fetch progress data based on selected filters."""
        if db is None:
            QMessageBox.critical(self, "Database Error", "Database connection is not available.")
            return

        client_id = self.client_id_input.text().strip()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        if not client_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Client ID.")
            return

        try:
            progress_data = db.get_progress(client_id, start_date, end_date)

            if not progress_data:
                QMessageBox.warning(self, "No Data", "No progress data found for this client in the selected period.")
                return

            self.table.setRowCount(len(progress_data))
            for row, data in enumerate(progress_data):
                self.table.setItem(row, 0, QTableWidgetItem(data["date"]))
                self.table.setItem(row, 1, QTableWidgetItem(str(data["weight"])))
                self.table.setItem(row, 2, QTableWidgetItem(data["notes"]))

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load data: {e}")

    def export_to_pdf(self):
        """Export report data to a PDF file."""
        if db is None:
            QMessageBox.critical(self, "Database Error", "Database connection is not available.")
            return

        client_id = self.client_id_input.text().strip()
        if not client_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Client ID.")
            return

        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, f"Client Progress Report - ID {client_id}", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(40, 10, "Date", 1)
            pdf.cell(40, 10, "Weight (Kgs)", 1)
            pdf.cell(110, 10, "Notes", 1)
            pdf.ln()

            for row in range(self.table.rowCount()):
                pdf.cell(40, 10, self.table.item(row, 0).text(), 1)
                pdf.cell(40, 10, self.table.item(row, 1).text(), 1)
                pdf.cell(110, 10, self.table.item(row, 2).text(), 1)
                pdf.ln()

            pdf_filename = "client_progress_report.pdf"
            pdf.output(pdf_filename)
            QMessageBox.information(self, "Success", f"PDF Exported Successfully as {pdf_filename}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = ReportsWindow()
    window.show()
    app.exec_()
