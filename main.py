import os

# import sqlite3 as SQL
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp

# use helpers.py to report the errors
from helpers import apology, login_required

import random

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///qmath50.db")
# # Configure CS50 Library to use SQLite database
# db_con = SQL.connect("qmath50.db")
# db = db_con.cursor()

# at the top, the list needs to begin from 0 to start to count, so -1
counter = -1

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template("layout.html")


################################################# LOGIN #################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    #Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print(request.form.get("username"))
        print(request.form.get("password"))

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


################################################# LOGOUT #################################################
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


################################################# REGISTER #################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        user_name = request.form.get("username")
        password = request.form.get("password")
        pw_confirmation = request.form.get("confirmation")

        # Check if the username is available
        user_name_check = db.execute("SELECT * FROM users WHERE username = ?", user_name)

        # Password confirmation
        if password != pw_confirmation:
            return apology("password not match", 400)

        hash_password = generate_password_hash(password)

        if len(user_name_check) >= 1:
            return apology("username has been taken", 400)

        # Add user data into db then log the user in
        else:
            flash("Registered!")

            # Use SQL INSERT to add the data to db
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user_name, hash_password)

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            return redirect("/")

    return render_template("register.html")


################################################# Game #################################################
# @app.route('/game', methods=['GET', 'POST'])
# def game_index():
#     num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     random_list = random.sample(num_list, 10)
#     counter = 9
#     return render_template("game.html")
#
# @app.route('/process', methods=['POST'])
# def process():
#     test = 12
#     if request.form.get('low'):
#         low = int(request.form['low'])
#         print(f"getting low: {low}")
#         # return jinja_question=question
#         return render_template("game.html", jinja_question=test)



@app.route('/game', methods=['GET', 'POST'])
def game_index():
    num_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    random_list = random.sample(num_list, 9)



    if request.args.get('number_L'):
        number_L = request.args.get('number_L')
        print()
        print('number_L:', number_L)
        print(type(number_L))
        print()
        return jsonify({'js_number_L': number_L})


    if request.form.get('guess'):

        guess = int(request.form['guess'])
        print(f"getting low: {guess}")

        if guess > 0:
            global counter

            # prevent the list out of range
            if counter == 8:
                # global counter
                counter = -1

                print(counter)
            else:
                counter += 1
                print(f"counter{counter}")
                num = num_list[counter]
                number_R = (f"{num}")

                return jsonify({'display_number': number_R})

        #     test = int(request.form['low'])
        #     return render_template("game.html", jinja_question=test)
        # if low == 7:
        #     Message = ("This is 7")
        #     return jsonify({'inputError': Message})


        # return jinja_question=question


    return render_template("game.html")






if __name__ == "__main__":
    app.run(debug=True)