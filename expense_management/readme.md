#Expense Reporting Project

##Description
This project is a Python based command-line application . It uses SQLite3 for data storage and implements role base access control. A user can efficiently manage their personal expenses by adding, updating and deleting expenses. Admins have extended privileges allowing them to manage users, payment methods and categories.

##Features

- Multi-user Authentication with Role based (Admin/User) Access Control
- Add, update, delete and view expenses
- Create and manage users, payment methods and categories (Admin Only)
- CSV import/ export functionality of expenses
- Generate various reports on expenses

##Creation of Database

- A database is created if it does not also exist when the script is executed
- The SQL statements CREATE TABLE IF NOT EXISTS ensures that tables are only created if they do not already exist
- There are 4 primary tables in the database: users, expenses, categories and payment_methods
- 'PRAGMA foreign_keys = ON' ensures that there is referential integrity by checking all foreign key constraints before allowing insertion, updating or deletion of records.

##Schema

###users
-The Users table stores information about users who log into the system. Each user has a unique identifier and login credentials.
Fields:
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_name TEXT NOT NULL UNIQUE,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
password TEXT NOT NULL,
role TEXT NOT NULL

###categories
-The Categories table stores different types of expense categories.
Fields:
category_id INTEGER PRIMARY KEY AUTOINCREMENT,
category_name TEXT NOT NULL

###expenses
-The Expenses table stores all financial transactions logged by users. It connects to the Users, Categories, and Payment_Methods tables through foreign keys.
Fields:
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

###payment_methods
-The Payment_Methods table stores different modes of payment.
Fields:
payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
payment_method TEXT NOT NULL

##CLI Commands

###User Authentication Management

- login <username> <password>
  -Description: Authenticates the user with message "Login successful Welcome, username (role)"
  -Returns:
  None
  -Permissions: Available to all
  -Error Handling:

  - Invalid credentials return an error message
  - Already logged in: Displays "An account is already logged in.".

- logout
  -Description: Logs out the current user
  -Permissions: Available to all
  -Error Handling:
  -Ensures a user is logged in before executing

- list_users
  -Description: Displays all users registered in the system
  -Permissions: Admin Only
  -Error Handling:
  - Prevents unauthorised users from performing this action and displays a clear error message

###Admin Only Functions

-add_user <user_name> <full_name> <password> <role>
-Description: Adds a new user to the system with a specified role
-Permissions: Admin Only
-Error Handling:
-Prevents duplicate usernames, displays an error message
-Ensures only admins can execute

-add category <category_name>
-Description: Creates a new expense category
-Permissions: Admin Only
-Error Handling:
-Prevents adding duplicate payment methods
-Ensures on admin can execute

-add_payment_methods <method_name>
-Description: Adds a new payment method to the system
-Permissions: Admin only
-Error Handling:
-Prevents adding duplicate payment methods
-Ensures that only admins can execute

#List

- list_categories
  Description: Lists all categories and their ids
  -Permissions: All - Users should be able to see what categories exist to be able to add expenses
  -Error Handling:

- list_payment_methods
  -Description: Lists all payment methods and their ids
  -Permissions: All - Users should be able to see what payment_methods exist to be able to add expenses

###Expense Management

-add expense amt=<amount> cat=<category> pmt*method<payment_method> tag=<tag> date=[date] description=[description]
-Description: Records a new expense for logged in user
-Permisssions: Available to all
-Error Handling:
-Ensures the amount is a positive number
-Verifies that category and payment method exist in database before adding
-Verifies date format is YYYY-MM-DD
-Duplicate Entry Checking
-Additional: - In CLI for the string components of the text the user has to type with * instead of whitespace as an alternative to using ""

-list_expenses (filter by: category=[category_name], start=[start_date], end=[end_date], min_amt=[min_amount], max_amt=[max_amount], payment=[payment_method], username=[username])
-Description: Display the expenses based on applied filters
-Permissions:
-Regular users can only see their own expenses
-Admins can view all expenses or filter by a specific user
-Error Handling:
-Ensures start date is not before end date
-Checks if only allowed filters are passed
-Validates date format, correct category and payment method, and amount
-Prevents unauthorized users from viewing other users' expenses

-update_expense <expense_id> <field> <new_value>
-Description: Updates a specified field of an expense record
-Permissions: Users can update only their own expenses
-Error Handling:
-Ensures the expense exists before updating
-Validates that the new value that the user enters follows the expected format and constraints of that field
-Prevents unauthorized users from changing other users' expenses

-delete_expense <expense_id>
-Description: Deletes an expense record
-Permissions: Users can only delete their own expenses
-Error Handling:
-Ensures the expense exists before deletion
-Prevents unauthorized users from deleting other users' expenses

###import export to CSV

-import_expenses <file_path>
-Description: Import expense records from a CSV
-Permissions: Available to all - Each user can import their own expenses
-Error Handling: - duplicate entry - user must be logged in - data types and references must be correct

-export_csv <file_path>  
 -Description: Exports all expenses from the database to a CSV file
-Permissions: Available to all - Users can only export their own expenses, admins can choose to export specific user' expenses or all
-Error Handling: - if users try to export another user's they will receive an error message - if the admin enters a wrong username they will receive error message

##Reports

-top_expenses <N> <start_date> <end_date>
-Description: Displays top N highest expenses within a given date range
-Permissions: Available to all

-category_spending<category>
-Description: Displays total spending in a specifies category
-Permissions: Available to all

-above_average_expenses
-Description: Lists expenses that exceed the category wise average
-Permissions: Available to all

-monthly_category_spending
-Description: Displays the total spending per category for each month
-Permissions: Available to all

payment_method_usage
-Description: Summarizes total spending per payment method
-Permissions: Available to all

-report tag_expenses_count
-Description: Counts the no. of expenses grouped by tags
-Permissions: Available to all

-report highest_spender
-Description: Identifies the user with the highest total spending for each month
-Permissions:Available to all

-report frequent_category
-Description: Identifies the most frequently used expense category
-Permissions: Available to all
