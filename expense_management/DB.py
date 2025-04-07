import sqlite3

class Database:
    def __init__(self, db_name="tracker.db"):
        """Initialize the database connection."""
        self.db_name = db_name

    def connect(self):
        """Connect to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def initialize_database(self):
        """Create necessary tables."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
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

            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS payment_methods (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_method TEXT NOT NULL
            );
        """)

        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")

    def insert_sample_data(self):
        """Insert sample data into tables."""
        conn = self.connect()
        cursor = conn.cursor()

        # Sample Users
        users_data = [
            ("HunkKiller", "John", "Doe", "password123", "admin"),
            ("CutiePie", "Alice", "Smith", "alicepass", "user"),
            ("Misha_TheGreatWarrier_Princess", "Bob", "Johnson", "bobsecure", "user"),
            ("Donald_Trump", "Emma", "Davis", "emma123", "user"),
            ("Fan_Of_GunturuChicken", "Liam", "Brown", "liampass", "admin")
        ]
        cursor.executemany("INSERT OR IGNORE INTO users (user_name, first_name, last_name, password, role) VALUES (?, ?, ?, ?, ?)", users_data)

        # Sample Categories
        categories_data = [
            ("Food"), ("Transport"), ("Entertainment"), ("Shopping"),
            ("Health"), ("Rent"), ("Education"), ("Utilities"),
            ("Travel"), ("Miscellaneous")
        ]
        cursor.executemany("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", [(c,) for c in categories_data])

        # Sample Payment Methods
        payment_methods_data = [
            ("Credit Card"), ("Debit Card"), ("PayPal"), ("Cash"),
            ("Bank Transfer"), ("Google Pay"), ("Apple Pay"), ("Cryptocurrency"), ("BitCoin")
        ]
        cursor.executemany("INSERT OR IGNORE INTO payment_methods (payment_method) VALUES (?)", [(p,) for p in payment_methods_data])

        expenses_data = [
        (1, 3, '2024-01-15', 45.75, 'Movie', 'Watched a new action film', 2),
        (1, 5, '2024-02-10', 120.50, 'Doctor', 'Annual health checkup', 1),
        (1, 1, '2024-03-05', 15.30, 'Dinner', 'Pizza night with friends', 3),
        (1, 2, '2024-04-20', 10.00, 'Bus', 'Commute to work', 4),
        (1, 4, '2024-05-12', 85.00, 'Shoes', 'New running shoes', 5),
        (1, 7, '2024-06-18', 200.00, 'Course', 'Enrolled in Python Bootcamp', 6),
        (1, 6, '2024-07-25', 800.00, 'Rent', 'Monthly apartment rent', 7),
        (1, 9, '2024-08-08', 250.00, 'Vacation', 'Weekend trip to the beach', 8),
        (1, 10, '2024-09-30', 50.00, 'Random', 'Miscellaneous shopping', 3),
        (1, 8, '2024-10-22', 95.00, 'Electricity', 'Monthly power bill', 4),

        (2, 1, '2024-01-05', 25.00, 'Groceries', 'Bought fruits and veggies', 2),
        (2, 3, '2024-02-14', 60.00, 'Valentine’s Dinner', 'Dinner with partner', 1),
        (2, 5, '2024-03-22', 300.00, 'Dentist', 'Teeth cleaning and checkup', 4),
        (2, 6, '2024-04-11', 750.00, 'Rent', 'Monthly apartment rent', 7),
        (2, 7, '2024-05-30', 100.00, 'Books', 'Bought new books online', 6),
        (2, 8, '2024-06-17', 85.00, 'Internet', 'Monthly WiFi bill', 5),
        (2, 4, '2024-07-08', 40.00, 'Clothes', 'Bought a new dress', 3),
        (2, 9, '2024-08-21', 150.00, 'Flights', 'Booked a ticket to New York', 2),
        (2, 2, '2024-09-19', 12.00, 'Taxi', 'Ride home from the airport', 8),
        (2, 10, '2024-10-25', 20.00, 'Random', 'Impulse buy at the mall', 1),

        (3, 3, '2024-01-11', 30.00, 'Concert', 'Attended music festival', 2),
        (3, 5, '2024-02-05', 50.00, 'Gym', 'Monthly membership renewal', 3),
        (3, 1, '2024-03-20', 18.00, 'Lunch', 'Fast food meal', 4),
        (3, 2, '2024-04-25', 8.50, 'Subway', 'Travel pass for work', 1),
        (3, 6, '2024-05-18', 900.00, 'Rent', 'Apartment rent', 7),
        (3, 7, '2024-06-22', 55.00, 'Workshop', 'Attended AI workshop', 6),
        (3, 9, '2024-07-28', 400.00, 'Travel', 'Flight ticket for vacation', 5),
        (3, 8, '2024-08-16', 70.00, 'Water Bill', 'Monthly bill payment', 8),
        (3, 10, '2024-09-14', 25.00, 'Misc', 'Bought new kitchen tools', 3),
        (3, 4, '2024-10-01', 120.00, 'Shopping', 'New headphones', 2),

        (4, 1, '2024-01-08', 65.00, 'Dining', 'Expensive steak dinner', 1),
        (4, 3, '2024-02-25', 40.00, 'Sports', 'Football tickets', 2),
        (4, 5, '2024-03-15', 200.00, 'Doctor', 'Specialist visit', 3),
        (4, 2, '2024-04-30', 15.00, 'Uber', 'Ride to a conference', 4),
        (4, 6, '2024-05-21', 1200.00, 'Rent', 'Luxury penthouse rent', 7),
        (4, 7, '2024-06-10', 350.00, 'Education', 'Business workshop', 6),
        (4, 9, '2024-07-05', 500.00, 'Holiday', 'Weekend in Miami', 5),
        (4, 8, '2024-08-20', 60.00, 'Gas', 'Filled up the car', 8),
        (4, 4, '2024-09-28', 95.00, 'Fashion', 'New designer suit', 2),
        (4, 10, '2024-10-14', 30.00, 'Impulse', 'Bought random gadgets', 1),

        (5, 1, '2024-01-02', 25.00, 'Fast Food', 'Bought fried chicken', 3),
        (5, 3, '2024-02-18', 50.00, 'Concert', 'Rock band live event', 1),
        (5, 5, '2024-03-10', 100.00, 'Medical', 'Bought medicine', 2),
        (5, 2, '2024-04-05', 9.00, 'Bus', 'Transport to hometown', 4),
        (5, 6, '2024-05-28', 950.00, 'Rent', 'Apartment rent', 7),
        (5, 7, '2024-06-14', 75.00, 'Workshop', 'Cooking class', 6),
        (5, 9, '2024-07-23', 300.00, 'Vacation', 'Travel to Thailand', 5),
        (5, 8, '2024-08-11', 85.00, 'Phone Bill', 'Monthly bill payment', 8),
        (5, 4, '2024-09-29', 40.00, 'Shopping', 'Bought a new watch', 2),
        (5, 10, '2024-10-07', 15.00, 'Misc', 'Random bookstore purchase', 1)
        ]

        cursor.executemany("INSERT OR IGNORE INTO expenses (user_id, category_id, date, amount, tag, description, payment_id) VALUES (?, ?, ?, ?, ?, ?, ?)", expenses_data)

        conn.commit()
        conn.close()
        print("✅ Sample data inserted successfully!")

