import sqlite3

class Database:
    def __init__(self, db_name="tracker.db"):
        """Initialize database name."""
        self.db_name = db_name

    def connect(self):
        """Create and return a database connection."""
        return sqlite3.connect(self.db_name)

    def initialize_database(self):
        """Create database tables if they do not already exist."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS payment_methods (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_method TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS expenses (
                expenses_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                date DATE NOT NULL,
                amount FLOAT NOT NULL,
                tag TEXT NOT NULL,
                description TEXT,
                payment_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (category_id) REFERENCES categories(category_id),
                FOREIGN KEY (payment_id) REFERENCES payment_methods(payment_id)
            );
        """)

        conn.commit()
        conn.close()


