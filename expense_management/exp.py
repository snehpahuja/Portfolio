

import sqlite3
import datetime
import csv


user_id = 1
current_user = None


from DB import Database  # Import the Database class from the 'database.py' file

# Now you can instantiate and use the Database class
db = Database()

# Initialize the database (if not already initialized)
db.initialize_database()

# Insert sample data (if needed)
#db.insert_sample_data()

# Connect to the database and perform your operations
with sqlite3.connect(db.db_name) as conn:
    cursor = conn.cursor()    
    def login(username, password):
        global current_user
        if not current_user:
            cursor.execute(
                "SELECT user_id, user_name, role FROM users WHERE user_name = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            if user:
                current_user = {"id": user[0], "user_name": user[1], "role": user[2]}
                print(f"✅Login successful! Welcome, {user[1]} ({current_user['role']})")
            else:
                print("❌Invalid credentials!")
        else:
            print("An account is already logged in.")
            
    def logout():
        global current_user
        if current_user:
            print(f"✅User {current_user['user_name']} logged out.")
            current_user = None
        else:
            print("❌No user is currently logged in.")

            
    def list_users():
        if current_user and current_user['role'] == 'admin':
            cursor.execute("SELECT user_id, first_name, last_name, role FROM users")
            users = cursor.fetchall()
            for user in users:
                print(f"ID: {user[0]}, Name: {user[1]} {user[2]}, Role: {user[3]}")
        else:
            print("❌ Access denied. Admins only.")


    def export_csv(filename, username=None, sort_field="date"):
        global current_user
        if not current_user:
            print("You must be logged in to export expenses.")
            return

        # Allowed sortable fields (excluding expense_id and user_id)
        allowed_sort_fields = {
            "category": "c.category_name", "date": "e.date",
            "amount": "e.amount", "tag": "e.tag",
            "description": "e.description", "payment": "p.payment_method"
        }
        
        sort_field = allowed_sort_fields.get(sort_field, "e.date")
        if sort_field == "e.date":
            print(f"No sort field given. Defaulting to 'date'.")

        # Base query
        query = """
            SELECT c.category_name, e.date, e.amount, e.tag, 
                   e.description, p.payment_method
            FROM expenses e
            LEFT JOIN categories c ON e.category_id = c.category_id
            LEFT JOIN payment_methods p ON e.payment_id = p.payment_id
        """
        params = []

        # Filtering logic
        if current_user['role'] == "admin":
            if username:
                cursor.execute("SELECT user_id FROM users WHERE user_name=?", (username,))
                user_id = cursor.fetchone()
                if not user_id:
                    print(f"❌ User {username} does not exist.")
                    return
                query += " WHERE e.user_id = ?"
                params.append(user_id[0])
            else:
                # If admin and no username provided, export all expenses
                print("⚠️ No username provided. Exporting all expenses.")
        elif current_user['role'] != "admin":
            if username:
                print("❌ Access Denied")
                return
            query += " WHERE e.user_id = ?"
            params.append(current_user['id'])

        query += f" ORDER BY {sort_field} ASC"
        
        # Execute and write to CSV
        cursor.execute(query, params)
        expenses = cursor.fetchall()
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["category", "date", "amount", "tag", "description", "payment_method"])
            writer.writerows(expenses)

        print(f"✅ Exported to {filename}, sorted by '{sort_field.split('.')[-1]}'.")


    def duplicate_check(user_id, amount, category_id, payment_id, date, description, tag):
        """Check if the expense already exists in the database."""
        cursor.execute("""
            SELECT COUNT(*) FROM expenses 
            WHERE user_id = ? AND amount = ? AND category_id = ? 
            AND payment_id = ? AND date = ? AND description = ? AND tag = ?
        """, (user_id, amount, category_id, payment_id, date, description, tag))
        
        return cursor.fetchone()[0] > 0  # Returns True if a duplicate exists

    def import_csv(filename):
        global current_user

        if not current_user:
            print("❌ You must be logged in to import expenses.")
            return

        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            valid_entries = []
            seen_entries = set()  # To track duplicates in the CSV file itself
            
            for row in reader:
                print(row)  # Print each row to inspect the contents
                try:
                    # Use the logged-in user's ID
                    user_id = current_user['id']

                    # Lookup Category ID (from category name)
                    category_id = validate_category(row["category"])

                    # Validate and format Date
                    date = validate_date(row["date"])

                    # Validate Amount
                    amount = validate_amount(float(row["amount"]))

                    # Lookup Payment Method ID (from payment method name)
                    payment_id = validate_payment_method(row["payment_method"])

                    # Create a tuple representing the expense (to check for duplicates in the file)
                    expense_tuple = (user_id, amount, category_id, payment_id, date, row["description"], row["tag"])

                    # Check for duplicate entry in the CSV file
                    if expense_tuple in seen_entries:
                        print(f"⚠️ Skipping duplicate expense in CSV: {row}")
                        continue  # Skip this entry
                    seen_entries.add(expense_tuple)

                    # Check for duplicate entry in the database
                    if duplicate_check(*expense_tuple):
                        print(f"⚠️ Skipping duplicate expense (already in DB): {row}")
                        continue  # Skip this entry
                    
                    # Append valid row
                    valid_entries.append(expense_tuple)

                except ValueError as e:
                    print(f"⚠️ Error processing row {row}: {e}")

        # Insert valid expenses into the database
        if valid_entries:
            cursor.executemany(
                "INSERT INTO expenses (user_id, amount, category_id, payment_id, date, description, tag) VALUES (?, ?, ?, ?, ?, ?, ?)",
                valid_entries
            )
            conn.commit()
            print(f"✅ {len(valid_entries)} expenses imported successfully.")
        else:
            print("❌ No valid expenses to import.")






    #START OF ADMIN ONLY FUNCTIONS
    def add_user(user_name,full_name, password, role):
        full_name = full_name.split(maxsplit=1)  # Split into first and last name
        first_name = full_name[0]
        last_name = full_name[1] if len(full_name) > 1 else ""  # Handle single name case
        
        global current_user
        
        if current_user and current_user['role'] == 'admin':
            # Insert user into database
            cursor.execute("SELECT user_name FROM users WHERE user_name = ?", (user_name,))
            existing_user = cursor.fetchone()
            if existing_user:
                print(f"❌ Error: Username '{user_name}' already exists.")
                return
            cursor.execute(
            "INSERT INTO users (user_name,first_name, last_name, password, role) VALUES (?,?, ?, ?, ?)",
            (user_name,first_name, last_name, password, role),)
            conn.commit()
            print(f"✅ Success: added user {user_name} with role {role}")
        else:
            print("❌ Access denied. Admins only.")
                
                
    def add_category(category_name):
        global current_user
        if current_user and current_user['role'] == 'admin':  # Check if user exists and is admin
            cursor.execute("SELECT * FROM categories WHERE category_name = ?",(category_name,))
            already_existing_category = cursor.fetchone()
            
            if already_existing_category:
                    print("❌ Error: Category already exists")
                    return
            
            cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
            conn.commit()
            print(f"✅ Success: Added category '{category_name}'")
        else:
            print("❌ Access denied. Only admin has the right to add a new category")
            
    def add_payment_method(method_name):
        cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
        user_role = cursor.fetchone()

        if current_user and current_user['role'] == 'admin':  # Ensure user exists and is admin
            cursor.execute("SELECT * FROM payment_methods WHERE payment_method = ?",(method_name,))
            already_existing_method = cursor.fetchone()
            
            if already_existing_method:
                    print("❌ Error: Payment Method already exists")
                    return
            

            cursor.execute("INSERT INTO payment_methods (payment_method) VALUES (?)", (method_name,))
            print(f"✅ Success: Added payment method '{method_name}'")
            conn.commit()
        else:
            print("❌ Access denied. Only admin has the right to add a new payment method")
            
    #END OF ADMIN ONLY
            
    def list_categories():
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        for category in categories:
            print(category,"\n")

    def list_payment_methods():
        cursor.execute("SELECT * FROM payment_methods")
        methods = cursor.fetchall()
        for method in methods:
            print(method,"\n")
            
    def get_category_id(category):
        cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (category,))
        cat_id = cursor.fetchone()
        if cat_id is None:
            return None
        return cat_id[0]

    def get_pmt_id(payment_method):
        cursor.execute("SELECT payment_id FROM payment_methods WHERE payment_method = ?", (payment_method,))
        pmt_id = cursor.fetchone()
        if pmt_id is None:
            return None
        return pmt_id[0]
        

    def validate_amount(amount):
        """Ensures amount is a positive number."""
        try:
            amount = float(amount)  # Convert to float to handle both integers and decimals
            if amount <= 0:
                print("❌ Error: Amount must be a positive number.")
                return None
            return amount
        except ValueError:
            print("❌ Error: Amount must be a number.")
            return None


    def validate_category(category):
        """Ensures category exists and returns its ID."""
        cat_id = get_category_id(category)
        if cat_id is None:
            print(f" ❌ Error: Category '{category}' does not exist.")
            return None
        return cat_id

    def validate_payment_method(payment_method):
        """Ensures payment method exists and returns its ID."""
        pmt_id = get_pmt_id(payment_method)
        if pmt_id is None:
            print(f"❌ Error: Payment Method '{payment_method}' does not exist.")
            return None
        return pmt_id
        

    def validate_date(date):
        """Validates date format (YYYY-MM-DD)."""
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("❌ Incorrect Date: Format(YYYY-MM-DD)/Value")
            return None
            

    def add_expense(amt, cat, pmt_method, tag, date=None, description=""):
        global current_user
        """
        Adds an expense after validating input values while preventing duplicates.
        """
        if current_user:
            # Validate amount
            if not validate_amount(amt):
                return
                
            # Validate category and payment method
            cat_id = validate_category(cat)
            if cat_id is None:
                return
            pmt_id = validate_payment_method(pmt_method)
            if pmt_id is None:
                return

            # Validate or set default date
            if date is None:
                date = datetime.date.today().strftime('%Y-%m-%d')
            else:    
                date = validate_date(date)
                if date is None:
                    return

            # Check for duplicate before inserting
            if duplicate_check(current_user['id'], amt, cat_id, pmt_id, date, description, tag):
                print(f"⚠️ Expense already exists. Duplicate entry not added.")
                return
            
            # Insert into database
            query = """
            INSERT INTO expenses (user_id, amount, category_id, payment_id, date, tag, description) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """ 
            try:
                cursor.execute(query, (current_user['id'], amt, cat_id, pmt_id, date, tag, description))
                conn.commit()
                print("✅ Expense added successfully!")
            except Exception as e:
                print(f"❌ Error adding expense: {e}")

                

    def list_expenses(category=None, start=None, end=None, min_amt=None, max_amt=None, payment=None, username=None):
        global current_user

        if not current_user:
            print("❌ You must be logged in to see your expenses.")
            return

        # Admin can choose to see all expenses or only their own
        if current_user['role'] == "admin":
            if username:
                cursor.execute("SELECT user_id FROM users WHERE user_name=?", (username,))
                user_id = cursor.fetchone()
                if not user_id:
                    print(f"❌ Error: User {username} does not exist.")
                    return
                user_id = user_id[0]
                query = "SELECT * FROM expenses WHERE user_id = ?"
                params = [user_id]
            else:
                query = "SELECT * FROM expenses WHERE 1=1"  # Admin sees all expenses
                params = []
        else:
            if username:
                print("❌ Access Denied.")
                return
            else:
                query = "SELECT * FROM expenses WHERE user_id = ?"
                params = [current_user['id']]

        # Filters dictionary (Fix: Ensure column names match the database schema)
        filters = {
            "category_id = ?": category,
            "date >= ?": start,
            "date <= ?": end,
            "amount >= ?": min_amt,
            "amount <= ?": max_amt,
            "payment_id = ?": payment
        }

        # Validate filters and build query
        for column, value in list(filters.items()):  # Using list() to allow modification inside loop
            if value is not None:
                if column.startswith("category_id"):
                    value = validate_category(value)  # Convert category name to ID
                elif column.startswith("payment_id"):
                    value = validate_payment_method(value)  # Convert payment method name to ID
                elif "date" in column:
                    value = validate_date(value)
                elif "amount" in column:
                    value= validate_amount(value)
                if value is None:
                    print(f"❌ Invalid value for filter: {column}")
                    return

                query += f" AND {column}"
                params.append(value)

        # Ensure start_date <= end_date
        if start and end and end < start:
            print("❌ End Date cannot be before Start Date.")
            return

        cursor.execute(query, tuple(params))
        expenses = cursor.fetchall()

        # Display results
        if not expenses:
            print("No expenses found with the given filters.")
        else:
            for expense in expenses:
                print(expense)

                
    def update_expense(expense_id, field, new_value):
            """
            Updates a specific field of an expense record after validation.
            """
            
            
            valid_fields = ["amount", "category_id", "payment_id", "date", "tag", "description"]

            # Validate Field Name
            if field not in valid_fields:
                print(f"❌ Error: '{field}' is not a valid field to update.")
                return
            
               # Check if expense_id exists
            cursor.execute("SELECT expenses_id FROM expenses WHERE expenses_id = ?", (expense_id,))
            
            if not cursor.fetchone():
                print(f"❌ Error: Expense ID {expense_id} does not exist.")
                return
            
            # Check if expense_id exists
            cursor.execute("SELECT user_id FROM expenses WHERE expenses_id = ?", (expense_id,))
            
            user_id = cursor.fetchone()[0]
            if current_user and user_id == current_user['id']:
                # Apply appropriate validation
                if field == "amount" and not validate_amount(new_value):
                    return
                if field == "category_id":
                    new_value = validate_category(new_value)
                    if new_value is None:
                        return
                if field == "payment_id":
                    new_value = validate_payment_method(new_value)
                    if new_value is None:
                        return
                if field == "date":
                    new_value = validate_date(new_value)
                    if new_value is None:
                        return

                # Update Database
                query = f"UPDATE expenses SET {field} = ? WHERE expenses_id = ?"
                
                try:
                    cursor.execute(query, (new_value, expense_id))
                    conn.commit()
                    print(f"✅ Expense {expense_id} updated successfully!")
                except Exception as e:
                    print(f"❌ Error updating expense: {e}")
            else:
                print(f"❌ Access Denied.")
                
    def delete_expense(expense_id):
            # Check if the expense exists before deleting
            cursor.execute("SELECT expenses_id FROM expenses WHERE expenses_id = ?", (expense_id,))
            
            if not cursor.fetchone():
                print(f"❌ Error: Expense ID {expense_id} does not exist.")
                return
            
            # Check if expense_id exists
            cursor.execute("SELECT user_id FROM expenses WHERE expenses_id = ?", (expense_id,))
            
            user_id = cursor.fetchone()[0]
            if current_user and user_id== current_user['id']:
                # Delete the expense
                cursor.execute("DELETE FROM expenses WHERE expenses_id = ?", (expense_id,))
                conn.commit()
                
                print(f"✅ Expense {expense_id} deleted successfully!")
            else:
                print("❌ Access Denied.")


    # REPORTS

    #report top N
    def top_expenses(N, start_date, end_date):
        if current_user:
            start_date = validate_date(start_date)
            end_date = validate_date(end_date)
            
            if end_date < start_date:
                print("Error: End date cannot be before Start date")
                return

            query = '''
                SELECT e.expenses_id, e.amount, e.date, u.first_name, u.last_name, c.category_name
                FROM expenses e
                JOIN users u ON e.user_id = u.user_id
                JOIN categories c ON e.category_id = c.category_id
                WHERE e.date BETWEEN ? AND ?
            '''
            params = [start_date, end_date]

            if current_user["role"] == "user":
                query += " AND e.user_id = ?"
                params.append(current_user["id"])

            query += " ORDER BY e.amount DESC LIMIT ?"
            params.append(N)

            cursor.execute(query, params)
            expenses = cursor.fetchall()

            print(f"Top {N} highest expenses from {start_date} to {end_date}:")
            print("ID | Amount | Date | User | Category")
            for expense in expenses:
                print(f"{expense[0]} | {expense[1]} | {expense[2]} | {expense[3]} {expense[4]} | {expense[5]}")
        else:
            print("❌ Error: You must be logged in.")

    def category_spending(category):
        if current_user:
            category_id = validate_category(category)
            if category_id:
                query = "SELECT SUM(amount) FROM expenses WHERE category_id = ?"
                params = [category_id]

                if current_user["role"] == "user":
                    query += " AND user_id = ?"
                    params.append(current_user["id"])

                cursor.execute(query, params)
                total_spending = cursor.fetchone()[0] or 0  # Ensure None values are handled

                print(f"Total spending in category '{category}': {total_spending}")
        else:
            print("❌ Error: You must be logged in.")


    #Report expenses greater than the category average.
    def above_average_expenses():
        if not current_user:
            print("❌ Error: You must be logged in.")
            return

        user_filter = "WHERE user_id = ?" if current_user["role"] == "user" else ""
        params = [current_user["id"]] if current_user["role"] == "user" else []

        # Get category-wise average spending
        cursor.execute(f'''
            SELECT category_name, AVG(amount) FROM expenses
            JOIN categories ON expenses.category_id = categories.category_id
            {user_filter}
            GROUP BY category_name
        ''', params)

        category_avg = cursor.fetchall()

        for category, avg in category_avg:
            cursor.execute(f'''
                SELECT expenses_id, amount, tag, description
                FROM expenses
                JOIN categories ON expenses.category_id = categories.category_id
                WHERE category_name = ? AND amount > ?
                {("AND user_id = ?" if current_user["role"] == "user" else "")}
            ''', [category, avg] + (params if current_user["role"] == "user" else []))

            expenses = cursor.fetchall()
            print(f"\nExpenses greater than average {avg:.2f} for category '{category}':")
            for exp in expenses:
                print(f"ID: {exp[0]}, Amount: {exp[1]}, Tag: {exp[2]}, Description: {exp[3]}")


    def monthly_category_spending():
        if not current_user:
            print("❌ Error: You must be logged in.")
            return

        user_filter = "WHERE user_id = ?" if current_user["role"] == "user" else ""
        params = [current_user["id"]] if current_user["role"] == "user" else []

        cursor.execute(f'''
            SELECT strftime('%Y-%m', date) AS month, category_name, SUM(amount)
            FROM expenses
            JOIN categories ON expenses.category_id = categories.category_id
            {user_filter}
            GROUP BY month, category_name
            ORDER BY month
        ''', params)

        monthly_spending = cursor.fetchall()
        print("Monthly spending per category:")
        for month, category, total in monthly_spending:
            print(f"{month} | {category} | {total}")


    def payment_method_usage():
        if not current_user:
            print("❌ Error: You must be logged in.")
            return

        user_filter = "WHERE e.user_id = ?" if current_user["role"] == "user" else ""
        params = [current_user["id"]] if current_user["role"] == "user" else []

        cursor.execute(f'''
            SELECT pm.payment_method, SUM(e.amount) AS Total_Spending
            FROM expenses e
            JOIN payment_methods pm ON pm.payment_id = e.payment_id
            {user_filter}
            GROUP BY pm.payment_id
        ''', params)

        responses = cursor.fetchall()
        for payment_method, total_spending in responses:
            print(f"Payment Method: {payment_method}, Total Spending: {total_spending}")


    def tag_expenses_count():
        if not current_user:
            print("❌ Error: You must be logged in.")
            return

        user_filter = "WHERE user_id = ?" if current_user["role"] == "user" else ""
        params = [current_user["id"]] if current_user["role"] == "user" else []

        cursor.execute(f'''
            SELECT tag, COUNT(expenses_id) AS Total_expense_count
            FROM expenses
            {user_filter}
            GROUP BY tag
        ''', params)

        responses = cursor.fetchall()
        for tag, count in responses:
            print(f"Tag: {tag}, Number of Expenses: {count}")

    def highest_spender():
        if current_user and current_user['role'] == 'admin':
            query = '''
            SELECT month, user_id, total_spent
            FROM (
                SELECT strftime('%Y-%m', date) AS month,
                user_id,
                SUM(amount) AS total_spent,
                DENSE_RANK() OVER (
                PARTITION BY strftime('%Y-%m', date)
                ORDER BY SUM(amount) DESC)
                AS dense_rank
                FROM expenses
                GROUP BY month, user_id
            ) AS ranked_expenses
            WHERE dense_rank = 1;
            '''
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                for row in results:
                    month = row[0]
                    user_id = row[1]
                    total_spent = row[2]
                    print(f"Highest spender for {month}: User {user_id} with {total_spent:.2f}")
            else:
                print("No data found.") 
        else:
            print("❌ Error: Admin must be logged in.")

    def frequent_category():  
        if not current_user:
            print("❌ Error: You must be logged in.")
            return

        user_filter = "WHERE user_id = ?" if current_user["role"] == "user" else ""
        params = [current_user["id"]] if current_user["role"] == "user" else []

        query = f'''
            SELECT category_id, COUNT(*) AS frequency
            FROM expenses
            {user_filter}
            GROUP BY category_id
            ORDER BY frequency DESC
            LIMIT 1;
        '''

        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            category_id, frequency = result
            cursor.execute("SELECT category_name FROM categories WHERE category_id = ?", (category_id,))
            category_name = cursor.fetchone()[0]
            print(f"The most frequently used expense category is '{category_name}' with {frequency} occurrences.")
        else:
            print("No data found.")

        

def main():
    while True:
        try:
            command = input(">>> ").strip()
            if not command:
                continue

            args = command.split()
            cmd = args[0].lower()

            if cmd == "help":
                print("""
Available Commands:
    - help: Show this message
    - login <username> <password>: Authenticate user
    - logout: End user session
    - list_users: Show all users and roles (Admin only)
    - add_user <username> <full_name> <password> <role>: Add a new user (Admin only)
    - add_category <category_name>: Add a new expense category (Admin only)
    - list_categories: View available categories
    - add_payment_method <method_name>: Add a new payment method
    - list_payment_methods: View payment methods
    - add_expense amt=<amount> cat=<category> pmt_method=<payment_method> tag=<tag> date=[date] description=[description]: Add an expense *(use underscores instead of spaces for parameters like payment_method or description)*
    - update_expense <expense_id> <field> <new_value>: Update an expense
    - delete_expense <expense_id>: Delete an expense
    - list_expenses [filters]: View expenses with optional filters
        -  username=<username>: Show expenses for a specific user *(Admin only)*
        -  category=<name>: Show expenses from a specific category  
        -  payment=<method> : Show expenses paid using a specific method  
        -  tag=<tag> : Show expenses associated with a specific tag  
        -  min_amt=<amount> : Show expenses with an amount **greater than or equal to** the given value  
        -  max_amt=<amount> : Show expenses with an amount **less than or equal to** the given value  
        -  start=<YYYY-MM-DD> : Show expenses from this date onward  
        -  end=<YYYY-MM-DD> : Show expenses up to this date   

    - import_expenses <file_path>: Import expenses from CSV
    - export_csv filename=<file_path> username=[username] sort_field=[<field_name>]: Export expenses to CSV with optional username filter and sorting
    - report <type> [parameters]: Generate reports
        - top_expenses <N> <start_date> <end_date>: View top N expenses within a date range
        - category_spending <category>: View spending for a category
        - above_average_expenses: View expenses above the average
        - monthly_category_spending: View monthly spending per category
        - payment_method_usage: View usage statistics of payment methods
        - tag_expenses_count: Count expenses by tags
        - highest_spender: Identify the highest spender
        - frequent_category: Identify the most frequently used expense category
    - exit: Quit the program

                """)

            elif cmd == "exit":
                    print("Exiting...")
                    break

            elif cmd == "login" and len(args) == 3:
                username, password = args[1], args[2]
                login(username, password)

            elif cmd == "logout":
                logout()

            elif cmd == "list_users":
                list_users()

            elif cmd == "add_user" and len(args) >= 5:
                username = args[1]
                role = args[-1]  # Role is always the last argument
                password = args[-2]  # Password is the second last argument
                name_parts = args[2:-2]  # Capture everything between username and password

                # Ensure the full name contains exactly two words (first & last name)
                if len(name_parts) != 2:
                    print("❌ Error: Either Full name does not contain exactly two words (First and Last name) or all the arguments are not entered. Enter help to see usage")
                    return

                full_name = " ".join(name_parts)
                add_user(username, full_name, password, role)

            elif cmd == "add_category" and len(args) >= 1:
                category_name = " ".join(args[1:])
                add_category(category_name)

            elif cmd == "list_categories":
                list_categories()

            elif cmd == "add_payment_method" and len(args) > 1:
                method_names = " ".join(args[1:])  # Join all the arguments after the command into one string
                add_payment_method(method_names)

            elif cmd == "list_payment_methods":
                list_payment_methods()        

            elif cmd == "add_expense":
                # Define allowable filters
                allowable_filters = ["amt", "cat", "pmt_method", "tag", "date", "description"]
                
                # Initialize a dictionary to store the key-value pairs
                expense_data = {}
                current_key = None
                current_value = []

                # Loop through the arguments, ignoring the first one (command)
                for i, arg in enumerate(args[1:]):
                    
                    if "=" in arg:  # If it's a key-value pair
                        if current_key:  # If there's a previously collected value, store it
                            # Join multi-word arguments and store in the dictionary
                            expense_data[current_key] = " ".join(current_value).strip()
                            current_value = []  # Reset the list for the next value

                        key, value = arg.split("=", 1)

                        if key in allowable_filters:
                            current_key = key
                            value = value.strip()

                            # Special handling for 'amount' to make sure it's numeric
                            if key == "amt":
                                try:
                                    # Immediately store 'amount' as a float value
                                    expense_data[current_key] = float(value)
                                    current_key = None  # Prevent overwriting of 'amount'
                                except ValueError:
                                    print(f"❌ Error: Amount '{value}' must be a valid number.")
                                    return
                            else:
                                # Allow multiple words only for category, payment_method, tag, and description
                                if key in ["cat", "pmt_method", "tag", "description"]:
                                    current_value.append(value)  # Append multi-word arguments for these keys
                                else:
                                    # For date, store them directly as values
                                    expense_data[current_key] = value
                        else:
                            print(f"❌ Error: Invalid filter key '{key}'")
                            return
                    else:  # If it's not a key-value pair, append it to the current value
                        # Append multi-word arguments for allowed keys (category, pmt_method, tag, description)
                        if current_key in ["cat", "pmt_method", "tag", "description"]:
                            current_value.append(arg.strip())  # Append multi-word arguments for allowed keys

                # After the loop, make sure to add the last collected value if any
                if current_key:
                    expense_data[current_key] = " ".join(current_value).strip()

                # Validation: Check if required fields are present
                required_fields = ["amt", "cat", "pmt_method", "tag"]
                missing_fields = [field for field in required_fields if field not in expense_data]
                
                if missing_fields:
                    print(f"❌ Error: Missing required fields: {', '.join(missing_fields)}")
                    return
                
                # Call the add_expense function with the processed arguments
                add_expense(**expense_data)
            
            elif cmd == "update_expense" and len(args) == 4:
                expense_id, field, new_value = args[1], args[2], args[3]
                update_expense(expense_id, field, new_value)

            elif cmd == "delete_expense" and len(args) == 2:
                expense_id = args[1]
                delete_expense(expense_id)
            
            elif cmd == "list_expenses":
                filters = {}
                current_key = None
                current_value = []

                for arg in args[1:]:  # Ignore the command name
                    if "=" in arg:  # Check if argument is in key=value format
                        key, value = arg.split("=", 1)  # Split only on first '='
                        
                        # Check for numeric fields and convert accordingly
                        if key in ["min_amount", "max_amount"]:  # Convert numeric fields
                            try:
                                value = float(value)  # Convert to number
                            except ValueError:
                                print(f"❌ Error: {key} must be a valid number.")
                                return
                        elif key == "payment":  # Handle 'pmt_method' for multiple words
                            # For payment method, allow multi-word values
                            current_key = key
                            current_value.append(value.strip())  # Append multi-word argument
                        else:
                            filters[key] = value.strip()  # For other fields, directly store the value

                    else:  # If it's not a key-value pair, append it to the current value
                        if current_key == "payment":
                            current_value.append(arg.strip())  # Append to payment method if it's multi-word

                # After the loop, make sure to add the last collected value if any
                if current_key == "payment":
                    filters[current_key] = " ".join(current_value).strip()

                # Call the list_expenses function with the processed filters
                list_expenses(**filters)




            elif cmd == "import_expenses" and len(args) == 2:
                file_path = args[1]
                import_csv(file_path)

            elif cmd == "export_csv" and len(args) >= 2:
                file_path = args[1]
                username = None
                sort_field = "date"  # Default sorting field

                if len(args) > 2:
                    for arg in args[2:]:  # Loop through extra arguments
                        if "=" in arg:
                            key, value = arg.split("=", 1)
                            if key == "sort_field":
                                sort_field = value  # Extract sort field
                            elif key == "username":
                                username = value  # If no "=", assume it's the username

                export_csv(file_path, username, sort_field)


            elif cmd.startswith("report"):
                if len(args) < 2:
                    print("⚠️ Error: Missing report type. Available reports: top_expenses, category_spending, above_average_expenses, monthly_category_spending, payment_method_usage, tag_expenses_count, highest_spender, frequent_category.")
                    return
                
                report_type = args[1]

                if report_type == "top_expenses" and len(args) == 5:
                    top_expenses(int(args[2]), args[3], args[4])  # Example: report top_expenses 5 2024-01-01 2024-03-01
                elif report_type == "category_spending" and len(args) == 3:
                    category_spending(args[2])  # Example: report category_spending Food
                elif report_type == "above_average_expenses":
                    above_average_expenses()
                elif report_type == "monthly_category_spending":
                    monthly_category_spending()
                elif report_type == "payment_method_usage":
                    payment_method_usage()
                elif report_type == "tag_expenses_count":
                    tag_expenses_count()
                elif report_type == "highest_spender":
                    highest_spender()
                elif report_type == "frequent_category":
                    frequent_category()
                else:
                    print(f"⚠️ Error: Invalid report type '{report_type}'.")


            else:
                print("Invalid command! Type 'help' for a list of available commands.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()



    
