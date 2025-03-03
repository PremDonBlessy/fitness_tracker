# database/database.py

import mysql.connector

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",   # Change if needed
                user="root",        # Change if needed
                password="Welcome@123456",  # Change if needed
                database="fitness_tracker"  # Ensure this database exists!
            )
            self.cursor = self.conn.cursor()
            self.create_tables()
            print("✅ Database Connected Successfully")

        except mysql.connector.Error as e:
            print(f"❌ Database Connection Failed: {e}")
            self.conn = None

    def create_tables(self):
        """Create necessary tables if they do not exist."""
        if self.conn is None:
            print("⚠️ No database connection.")
            return

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                weight FLOAT,
                goal TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                reminder_date DATE,
                message TEXT,
                status VARCHAR(50),
                FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def get_reminders(self):
        """Fetch all reminders."""
        if self.conn is None:
            return []
        self.cursor.execute("SELECT client_id, reminder_date, message, status FROM reminders")
        return [{"client_id": row[0], "reminder_date": row[1], "message": row[2], "status": row[3]}
                for row in self.cursor.fetchall()]

    def save_reminder(self, client_id, reminder_date, message, status):
        """Save a new reminder."""
        if self.conn is None:
            return
        self.cursor.execute(
            "INSERT INTO reminders (client_id, reminder_date, message, status) VALUES (%s, %s, %s, %s)",
            (client_id, reminder_date, message, status)
        )
        self.conn.commit()

    def delete_reminder(self, client_id, reminder_date):
        """Delete a reminder."""
        if self.conn is None:
            return
        self.cursor.execute("DELETE FROM reminders WHERE client_id = %s AND reminder_date = %s",
                            (client_id, reminder_date))
        self.conn.commit()
