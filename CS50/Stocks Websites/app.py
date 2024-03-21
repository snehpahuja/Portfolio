import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd
import pytz


IST = pytz.timezone('Asia/Kolkata')

# Configure application
app = Flask(__name__)
app.debug = True
data_exists = False

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


userid = None

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    symbols = db.execute("SELECT symbol, shares FROM user_data WHERE user_id=?", session["user_id"])
    if symbols:
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        current_prices = []
        total_value = cash[0]["cash"]
        for symbol in symbols:
            values = lookup(symbol["symbol"])
            current_price = values["price"]
            total_price = current_price * symbol["shares"]
            total_value = total_value + total_price
            db.execute("UPDATE user_data SET price=?, total_price=? WHERE symbol=?", current_price, total_price, symbol["symbol"])
            db.execute("UPDATE users SET total_value=? WHERE id=?", total_value, session["user_id"])
        stock_values =  db.execute("SELECT * FROM user_data WHERE user_id=?", session["user_id"])
        total_value = db.execute("SELECT total_value FROM users WHERE id=?", session["user_id"])
        return render_template("index.html", stock_values=stock_values, cash=cash[0]["cash"], total_value=total_value[0]["total_value"])
    else:
        return render_template("emptyindex.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    """if user has submitted information """
    if request.method == "POST":
        symbol = request.form.get("symbol")
        values = lookup(symbol)
        shares = request.form.get("shares")
        """check whether the share the user has entered is a number"""
        is_int = True
        if shares.isdigit() == False:
             is_int = False
        if is_int == True:
          shares = int(shares)
          if not shares > 0:
              return apology("Shares must be greater than 0", 400)
          if values:
                 cash = db.execute("SELECT cash FROM users WHERE id= ?", session["user_id"] )
                 total_price = values["price"] * shares
                 if total_price > cash[0]["cash"]:
                        return apology("Not enough cash to make the purchase.", 400)
                 else:
                        new_cash = cash[0]["cash"] - total_price
                        db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, session["user_id"])
                        old_shares = db.execute("SELECT shares FROM user_data WHERE user_id=? AND symbol=?", session["user_id"], symbol)
                        if old_shares:
                                new_shares = old_shares[0]["shares"] + shares
                                db.execute("UPDATE user_data SET shares=? WHERE symbol=?", new_shares, symbol)
                        else:
                                new_shares = shares
                                db.execute("INSERT INTO user_data( user_id, symbol, name, shares) VALUES(?, ?, ?, ?)", session["user_id"], symbol, values["name"], new_shares)
                        date_time = datetime.now(IST)
                        db.execute("INSERT INTO history(user_id, symbol, shares, price, date_time) VALUES( ?, ? , ? , ? , ?)", session["user_id"], symbol, shares, values["price"], date_time )
                        return redirect("/")
          else:
              return apology("Please enter a valid symbol", 400)
        else:
             return apology("Please enter a valid share number", 400)
    else:
        return render_template("buy.html")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM history WHERE user_id=?", session["user_id"] )
    return render_template("history.html", transactions=transactions )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        user_id = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock_values = lookup(symbol)
        is_valid = False
        if stock_values:
            is_valid = True
            return render_template ("quote_stats.html", valid_status=is_valid, stock_values=stock_values)
        else:
            return apology ("Please enter a vaild symbol", 400)
    else:
        return render_template("quote_form.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            username_check = db.execute("SELECT username FROM users WHERE username=?", username)
            if username_check:
                return apology("Sorry. That username has already been chosen. Please choose another username.", 400)
            else:
                password = request.form.get("password")
                if password:
                    confirm_password = request.form.get("confirmation")
                    if (confirm_password == password):
                        hashed_password = generate_password_hash(password)
                        db.execute("INSERT INTO users( username, hash) VALUES( ?, ?)", username, hashed_password )
                        current_id = db.execute("SELECT id FROM users WHERE username=?", username)
                        session["user_id"] = current_id
                        return redirect("/login")

                    else:
                        return apology("Password and Confirmation must match", 400)
                else:
                    return apology("Password field cannot be left blank", 400)
        else:
            return apology("Username field cannot be left blank", 400)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if symbol:
             is_int = True
             if shares.isdigit() == False:
                is_int = False
                return apology("Shares must be a valid number", 400)
             else:
                if is_int == True:
                    shares = int(shares)
                    if not shares > 0:
                        return apology("Shares must be greater than 0", 400)

                    user_shares = db.execute("SELECT shares FROM user_data WHERE user_id=? AND symbol=?", session["user_id"], symbol)
                    if shares > user_shares[0]["shares"]:
                        return apology("You cannot select more shares than present", 400)
                    else:
                        cash = db.execute("SELECT cash FROM users WHERE id=?",session["user_id"])
                        values = lookup(symbol)
                        new_cash = cash[0]["cash"] + ( values["price"] * shares )
                        db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, session["user_id"])
                        if shares == user_shares[0]["shares"]:
                            db.execute("DELETE FROM user_data WHERE user_id=? AND symbol=?", session["user_id"], symbol)
                            return redirect("/")
                        else:
                            new_shares = user_shares[0]["shares"] - shares
                            db.execute("UPDATE user_data SET shares=? WHERE user_id=? AND symbol=?",new_shares, session["user_id"], symbol )
                            date_time = datetime.now();
                            shares = shares * -1
                            db.execute("INSERT INTO history(user_id, symbol, shares, price, date_time) VALUES( ?,  ? , ? , ? , ?)", session["user_id"], symbol, shares, values["price"], date_time)
                            return redirect("/")
        else:
            return apology("Missing Symbol", 400)
    else:
        stocks = db.execute("SELECT symbol FROM user_data WHERE user_id=?", session["user_id"] )
        return render_template("sell.html", stocks=stocks)

@app.route("/reset", methods=["GET", "POST"])
def reset():
    """ change password"""
    if request.method == "POST":
        username = request.form.get("username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        """ making sure no fields are left blank"""
        if not username:
            return apology("Username field cannot be left blank", 400)
        elif not old_password:
            return apology("Old Password field cannot be left blank", 400)
        elif not new_password:
            return apology("New Password field cannot be left blank", 400)
        elif not confirm_password:
            return apology("Confirm Password field cannot be left blank", 400)
        else:
            """ making sure the username and old password are valid"""
            validate_username = db.execute("SELECT * FROM users WHERE username=?", username)
            if validate_username:
                validate_password = db.execute("SELECT hash FROM users WHERE username=?", username)
                if check_password_hash(validate_password[0]["hash"], old_password) == False:
                    return apology("Incorrect Password", 400)
                """checking if the new password is not the same as the old"""
                if check_password_hash(validate_password[0]["hash"], new_password) == True:
                    return apology("New Password cannot be the same as the old password", 400)
                """making sure the new password and confirmation match"""
                if new_password != confirm_password:
                    return apology("New Password and Password confirmation do not match", 400)
                hashed_password = generate_password_hash(new_password)
                db.execute("UPDATE users SET hash=? WHERE username =?", hashed_password, username)
                return redirect("/")
            else:
                return apology("Invalid Username", 400)
    else:
        return render_template("reset.html")

@app.route("/wallet", methods=["GET", "POST"])
@login_required
def wallet():
    current_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            return apology("Please enter an amount to be added", 400)
        new_cash = int(amount) + current_cash[0]["cash"]
        db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, session["user_id"])
        return  render_template("wallet.html", current_cash=new_cash)
    else:
        return render_template("wallet.html", current_cash=current_cash[0]["cash"])

