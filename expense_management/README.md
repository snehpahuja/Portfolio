# Expense Reporting Project

## Description
This project is a Python-based command-line application that uses SQLite3 for data storage and implements role-based access control. Users can manage personal expenses by adding, updating, viewing, and deleting records. Admin users have extended privileges to manage users, payment methods, and categories.

---

## Features
- Multi-user authentication with role-based access (Admin / User)
- Add, update, delete, and view expenses
- Create and manage users, payment methods, and categories (Admin only)
- CSV import and export of expenses
- Generate analytical reports on spending

---

## Database Creation
- The database is created automatically if it does not already exist
- `CREATE TABLE IF NOT EXISTS` ensures tables are created safely without overwriting data
- Four primary tables:
  - `users`
  - `expenses`
  - `categories`
  - `payment_methods`
- `PRAGMA foreign_keys = ON` enforces referential integrity across tables

---

## Database Schema

### Users
Stores information about users who log into the system.

**Fields:**
- `user_id` INTEGER PRIMARY KEY AUTOINCREMENT  
- `user_name` TEXT NOT NULL UNIQUE  
- `first_name` TEXT NOT NULL  
- `last_name` TEXT NOT NULL  
- `password` TEXT NOT NULL  
- `role` TEXT NOT NULL  

---

### Categories
Stores expense categories.

**Fields:**
- `category_id` INTEGER PRIMARY KEY AUTOINCREMENT  
- `category_name` TEXT NOT NULL  

---

### Expenses
Stores all financial transactions logged by users.

**Fields:**
- `expenses_id` INTEGER PRIMARY KEY AUTOINCREMENT  
- `user_id` INTEGER NOT NULL  
- `category_id` INTEGER NOT NULL  
- `date` DATE NOT NULL  
- `amount` FLOAT NOT NULL  
- `tag` TEXT NOT NULL  
- `description` TEXT  
- `payment_id` INTEGER NOT NULL  

**Foreign Keys:**
- `user_id` → `users(user_id)`  
- `category_id` → `categories(category_id)`  
- `payment_id` → `payment_methods(payment_id)`  

---

### Payment Methods
Stores modes of payment.

**Fields:**
- `payment_id` INTEGER PRIMARY KEY AUTOINCREMENT  
- `payment_method` TEXT NOT NULL  

---

## CLI Commands

### User Authentication
#### `login <username> <password>`
- Authenticates the user and displays role-based confirmation
- Error handling:
  - Invalid credentials
  - Prevents multiple active logins

#### `logout`
- Logs out the current user
- Ensures a user is logged in before execution

#### `list_users`
- Displays all registered users
- **Admin only**
- Prevents unauthorized access

---

### Admin Commands

#### `add_user <username> <full_name> <password> <role>`
- Adds a new user
- Prevents duplicate usernames
- **Admin only**

#### `add_category <category_name>`
- Adds a new expense category
- Prevents duplicates
- **Admin only**

#### `add_payment_method <method_name>`
- Adds a new payment method
- Prevents duplicates
- **Admin only**

---

### Reference Lists

#### `list_categories`
- Displays all categories and their IDs
- Available to all users

#### `list_payment_methods`
- Displays all payment methods and their IDs
- Available to all users

---

## Expense Management

#### `add_expense amt=<amount> cat=<category> pmt_method=<payment_method> tag=<tag> date=[date] description=[description]`
- Adds a new expense for the logged-in user
- Validations:
  - Positive amount
  - Valid category and payment method
  - Date format `YYYY-MM-DD`
  - Duplicate entry checks

> Note: Use underscores instead of spaces for multi-word inputs in the CLI.

---

#### `list_expenses`
**Optional filters:**
- `category`
- `start`
- `end`
- `min_amt`
- `max_amt`
- `payment`
- `username` (Admin only)

**Permissions:**
- Users see only their own expenses
- Admins can view all or filter by user

---

#### `update_expense <expense_id> <field> <new_value>`
- Updates a specific expense field
- Users can update only their own expenses
- Validates format and permissions

---

#### `delete_expense <expense_id>`
- Deletes an expense
- Users can delete only their own expenses

---

## CSV Import / Export

#### `import_expenses <file_path>`
- Imports expenses from a CSV file
- Validates:
  - User login
  - Data types
  - Foreign key references
  - Duplicate entries

---

#### `export_csv <file_path> [username]`
- Exports expenses to CSV
- Users export only their own data
- Admins may export all users or a specific user

---

## Reports

#### `top_expenses <N> <start_date> <end_date>`
- Displays top N expenses in a date range

#### `category_spending <category>`
- Displays total spend for a category

#### `above_average_expenses`
- Lists expenses above category average

#### `monthly_category_spending`
- Shows monthly totals per category

#### `payment_method_usage`
- Summarizes spending by payment method

#### `report tag_expenses_count`
- Counts expenses grouped by tags

#### `report highest_spender`
- Identifies the highest spender per month (Admin)

#### `report frequent_category`
- Identifies the most frequently used category

