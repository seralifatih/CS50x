import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/history")
@login_required
def history():

    stocks = db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER BY date DESC", user_id=session["user_id"])

    return render_template("history.html", stocks=stocks)


@app.route("/")
@login_required
def index():

    stocks = db.execute("SELECT * FROM stocks WHERE user_id = :user_id ORDER BY symbol ASC", user_id=session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    #quantity = stocks[2]
    grand_total = 0.0

    for i in range(len(stocks)):
        stock = lookup(stocks[i]["symbol"])
        stocks[i]["company"] = stock["name"]
        stocks[i]["quantity"] = stocks[i]["quantity"]
        stocks[i]["cur_price"] = "%.2f"%(stock["price"])
        stocks[i]["total"] = "%.2f"%(stocks[i]["total"])

    grand_total += float(user[0]["cash"])

    return render_template("index.html", stocks=stocks, cash=usd(user[0]["cash"]), grand_total=usd(grand_total))


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    stocks = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])

    if request.method == "POST":
        user_id = session["user_id"]

        #number of shares cannot be empty
        if not request.form.get("shares"):
            return apology("number of shares cannot be empty")

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a positive integer", 400)

        symbol = request.form.get("symbol").upper()

        #dictionary indicating the stock name, symbol and current price
        stock = lookup(symbol)

        #store the stock symbol in a variable
        symbol = stock["symbol"] #string

        #eski user_info
        stock_info = db.execute("SELECT * FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
        user_id=user_id, symbol=symbol)

        #eski personal_info
        user_info = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)

        #number of stocks owned by the user
        owned_quantity = stock_info[0]["quantity"]

        #store stock price in a variable as a float
        stock_price = float(stock["price"])

        #store the number of shares requested to be sold by the user
        quantity_to_be_sold = int(request.form.get("shares"))

        #calculate total cash to be received by the user
        value = stock_price * quantity_to_be_sold

        #calculate remaining cash
        remaining_cash = float(user_info[0]["cash"]) + (stock_price * quantity_to_be_sold)

        #calculate remaining quantity
        remaining_quantity = owned_quantity - quantity_to_be_sold

        #calculate remaining value of the stocks
        new_total = remaining_quantity * stock_price

        if stock_info:
            stock_info = stock_info[0]
        else:
            return render_template("sell.html", stocks=stocks)

        if quantity_to_be_sold > stock_info["quantity"]:
            return apology("you don't have enough stocks")
        else:
            #remaining_quantity = int(stock_db["quantity"]) - int(quantity_to_be_sold)
            #new_total = float(personal_info[0]["cash"]) - value

            #update existing records
            db.execute("UPDATE stocks SET quantity = :quantity, total = :total WHERE user_id = :user_id AND symbol = :symbol",
            quantity=remaining_quantity, total=new_total, user_id=user_id, symbol=symbol)
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=remaining_cash, user_id=user_id)

            #if quantity is 0, delete record
            new_stocks = db.execute("SELECT * FROM stocks WHERE user_id =:user_id AND symbol=:symbol",
            user_id=user_id, symbol=symbol)
            new_quantity = new_stocks[0]["quantity"]
            if new_quantity == 0:
                db.execute("DELETE FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
                user_id=user_id, symbol=symbol)

            #update history
            action="Sold"
            db.execute("INSERT INTO history (user_id, action, symbol, quantity, total) VALUES (:user_id, :action, :symbol, :quantity, :total)",
                        user_id=user_id, action=action, symbol=symbol, quantity=quantity_to_be_sold, total=value)

            return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        #store user id in a variable. from: https://www.reddit.com/r/cs50/comments/5p30yc/pset7_sql_lookup_current_user/dcp1y2z/
        user_id = session["user_id"]

        #dictionary indicating the stock name, symbol and price
        stock = lookup(request.form.get("symbol"))

        #make sure the user does not leave the symbol and shares fields empty
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("stock name and/or number of shares cannot be empty")

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if int(shares) < 1:
            return(apology("invalid number"))

        #check whether the stock symbol is valid based on the above stock dictionary
        if stock == None:
            return apology("invalid stock symbol")

        #store stock price in a variable as a float
        stock_price = stock["price"]

        #check the current cash of the user
        user_info = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
        cash = user_info[0]["cash"]

        #store the number of shares requested by the user in a variable
        quantity = int(request.form.get("shares"))

        #calculate total price
        total_price = float(stock["price"]) * float(quantity)

        #store the stock symbol in a variable
        symbol = stock["symbol"] #string

        #process purchase if there is sufficient cash
        if cash >= (stock_price * quantity):
            #update user's remaining cash
            remaining_cash = int(cash) - (stock_price * quantity)

            #check if the stock is already owned
            stock_db = db.execute("SELECT * FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
            user_id=user_id, symbol=symbol)

            #if owned, updatew with the new purchase
            if len(stock_db) == 1:

                new_quantity = int(stock_db[0]["quantity"]) + int(quantity)
                new_total = float(stock_db[0]["total"]) + total_price
                new_pps = "%.2f"%(new_total / float(new_quantity))

                #update existing record
                db.execute("UPDATE stocks SET quantity = :quantity, total = :total, pps = :pps WHERE user_id = :user_id AND symbol = :symbol",
                quantity=new_quantity, total=new_total, pps=new_pps, user_id=user_id, symbol=symbol)
                db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=remaining_cash, user_id=user_id)
                action="Bought"
                db.execute("INSERT INTO history (user_id, action, symbol, quantity, total) VALUES (:user_id, :action, :symbol, :quantity, :total)",
                user_id=user_id, action=action, symbol=symbol, quantity=quantity, total=total_price)
                return redirect("/")
            else:
                #create new record
                db.execute("INSERT INTO stocks (user_id, symbol, quantity, total, pps) VALUES (:user_id, :symbol, :quantity, :total, :pps)",
                user_id=user_id, symbol=symbol, quantity=quantity, total=total_price, pps=stock["price"])
                db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=remaining_cash, user_id=user_id)

                #update history  FIX THIS
                action = "Bought"
                db.execute("INSERT INTO history (user_id, action, symbol, quantity, total) VALUES (:user_id, :action, :symbol, :quantity, :total)",
                user_id=user_id, action=action, symbol=symbol, quantity=quantity, total=total_price)

                return redirect("/")
        else:
            return apology("insufficient funds!")

    else:
        return render_template("buy.html")



@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("Stock could not be found")
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


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

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        #ensure username is inserted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        #ensure password is inserted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        #make sure password is confirmed through second entry
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("must confirm password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        #check from database if the username already taken
        if len(rows) == 1:
            return apology("username already taken", 400)

        password = (request.form.get("password"))

        #ensure password contains numbers
        numbers = 0
        for i in range(len(password)):
            if str(i).isnumeric() == True:
                numbers += 1
        if numbers == 0:
            return apology("password must contain numbers as well")

        #if it isn't taken, insert the username and password cash into database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

            #log the user in and return to homepage
            user_row = db.execute("SELECT id FROM users WHERE username = :username", username=request.form.get("username"))
            session["user_id"] = user_row[0]["id"]
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
