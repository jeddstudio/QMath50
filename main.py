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

import time
from datetime import datetime

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
# sqlite3 moudel SQL database
# db_con = SQL.connect("qmath50.db")
# db = db_con.cursor()

# at the top, cause webpage R_numb start with 1 already 
# just needs to begin from 2 to start in the list, so set counter=1
counter = 1
# The Display number on the page, for calculation
number_L = 1
number_R = 1
start_time = 0
end_time = 0



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

################################################# INDEX #################################################
@app.route('/')
@login_required
def index():
    """Show profile page"""
    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]

       
        # Set a list for export data to Jinja
        best_time_list = []

        # Loop 2-19, range is a counter for db.execute
        for data in range(2,20):
            # No need 10 × 10 in the game
            if data == 10:
                pass
            else:
                # Set a dict to hold the processed data
                temp_dict = {}

                # Get best_time of the game_type 1 by 1
                best_time_db = db.execute("SELECT game_type, MIN(best_time), time FROM profile WHERE pofo_id = ? AND game_type = ?", acc_id, data)

                # best_time_db will look like:
                # [{'game_type': '2', 'MIN(best_time)': 4.045}]
                
                # Grab the data only from [{'game_type': '2', 'MIN(best_time)': 4.045}]
                game_type = best_time_db[0]["game_type"]
                # game_type = 2
                best_time = best_time_db[0]["MIN(best_time)"]
                # best_time = 4.045
                record_date_time = best_time_db[0]["time"]
                # record_date_time = 2022-11-15 09:54:32

                # Put these into temp_dict and create a key ["game_type"] and ["best_time"]
                temp_dict["game_type"] = game_type
                temp_dict["best_time"] = best_time
                temp_dict["time"] = record_date_time
                # temp_dict will look like:
                # {'game_type': '2', 'best_time': 4.045, 'time': '2022-11-15 09:54:32'}
                
                # game_type is for display on the webpage like 2 × 2 using Jinja
                if temp_dict["game_type"] == None:
                    temp_dict["game_type"] = data
                # If best_time not None, add a unit "s" for display on webpage
                if temp_dict["best_time"] != None:
                    temp_dict["best_time"] = str(best_time) + "s"

                # Add temp_dict: {'game_type': '2', 'best_time': 4.045, 'time': '2022-11-15 09:54:32'} into the best_time_list
                best_time_list.append(temp_dict)

        # Get a list of dictionaries like:
        # [{'game_type': '2', 'best_time': '4.045s', 'time': '2022-11-15 09:54:32'}, {'game_type': '3', 'best_time': '8.752s', 'time': '2022-11-16 13:10:46'}, ....]
        contents = best_time_list

        return render_template("index.html", jinja_username=username, jinja_contents=contents)

    else:
        return render_template("login.html")



################################################# Rank #################################################
@app.route('/rank')
@login_required
def rank():
    """Show profile page"""
    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]

    
        # Set a list for export data to Jinja
        best_time_list = []

        # Loop 2-19, range is a counter for db.execute
        for data in range(2,20):
            # No need 10 × 10 in the game
            if data == 10:
                pass
            else:
                # Set a dict to hold the processed data
                temp_dict = {}

                # Get best_time of the game_type 1 by 1
                rank_best_db = db.execute("SELECT game_type, pofo_id, MIN(best_time), time FROM profile WHERE game_type = ?", data)
                # rank_best_db will look like:
                # [{'game_type': '2', 'pofo_id': 1, 'MIN(best_time)': 4.045, 'time': '2022-11-15 09:54:32'}]
                
                # Grab the id for getting the username from the users table in SQL
                best_player_id = rank_best_db[0]["pofo_id"]
                # best_player_id will a number only, e.g. 1, 6


                best_player_name = db.execute("SELECT username FROM users WHERE id = ?", best_player_id)
                # It will look like: [{'username': 'GM_1'}]

                # If there is no data in the Database, None is displayed
                # Check if the best_player_name = [], it will be true
                if not best_player_name:
                    # game_type is for display on the webpage like 2 × 2 using Jinja
                    game_type = data
                    # Others data is display for None
                    player_name = None
                    best_time = None
                    record_date_time = None 
                else:
                    game_type = rank_best_db[0]["game_type"]
                    # 9
                    player_name = best_player_name[0]["username"]
                    # GM_1
                    best_time = rank_best_db[0]["MIN(best_time)"]
                    # 22.494
                    record_date_time = rank_best_db[0]["time"]
                    # 2022-11-17 23:00:12
                

                # Put these into temp_dict and create a key ["game_type"], ["username"], ["best_time"] and ["time"]
                temp_dict["game_type"] = game_type
                temp_dict["username"] = player_name
                temp_dict["best_time"] = best_time
                temp_dict["time"] = record_date_time

                # If best_time not None, add a unit "s" for display on webpage
                if temp_dict["best_time"] != None:
                    temp_dict["best_time"] = str(best_time) + "s"
                
                # Add temp_dict: {'game_type': '2', 'username': '111', 'best_time': '4.045s', 'time': '2022-11-15 09:54:32'} into the best_time_list
                best_time_list.append(temp_dict)


        # Get a list of dictionaries like:
        # [{'game_type': '2', 'username': '111', 'best_time': '4.045s', 'time': '2022-11-15 09:54:32'}, {'game_type': '3', 'username': 'GM_1', 'best_time': '8.539s', 'time': '2022-11-17 22:57:23'},  ....]
        contents = best_time_list

        return render_template("rank.html", jinja_username=username, jinja_contents=contents)

    else:
        return render_template("login.html")




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


################################################# Basic Game #################################################
@app.route('/game', methods=['GET', 'POST'])
@login_required
def game_basic():

    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]

    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random_list = random.sample(num_list, 9)

    global number_L
    global start_time
    global number_R
    global end_time
    global counter

    # Get number_L from form.js
    if request.args.get('number_L'):

        # If the user presses the refresh button in the middle of the game, it resets all Global value
        if start_time != 0 and number_R > 1:
            number_R = 1
            start_time = 0
            end_time = 0
            counter = 1
            number_L = int(request.args.get('number_L'))
            return jsonify({'js_number_L': number_L})
        # If not, normally to running the game
        else:
            number_L = int(request.args.get('number_L'))
            return jsonify({'js_number_L': number_L})


    # When user input a number and press Enter
    # Get guess from form.js
    if request.form.get('js_guess'):

        answer = number_L * number_R
        guess = int(request.form['js_guess'])

        # Save the start time when user input(and press Enter) first answer
        if counter == 1:
            start_time = time.time()
            print("1 START: ", start_time)

        # When the last answer is correct, Game End 
        if answer == guess and counter == 10:
            # Calculating Time
            end_time = time.time()
            print("END: ", end_time)
            total_time = float("{:.3f}".format((end_time - start_time)))
            print(f"time_lapsed:{end_time} - {start_time}")
            # Reset the Global values
            counter = 1
            number_R = 1
            date_time = datetime.now()
            print("Stopwatch: ", total_time)
            # Show a game end message and Reset the num_R to 1


            ############### SQL part ###############
            # SQL only save the best_time record when the current time faster than SQL's fastest record

            # Check if the best_time is exists in db or NOT
            data_check = db.execute("SELECT best_time FROM profile WHERE EXISTS(SELECT * FROM profile WHERE pofo_id = ? AND game_type = ?)", acc_id, number_L)
            # This is to check if data already exists. It will return [{'best_time': 4.441}, {'best_time': 9.717}]
            # So if it len(data_check) == 0, it means there is no data

            # If the best_time does NOT exist, use SQL INSERT to add a record
            if len(data_check) == 0:
                db.execute("INSERT INTO profile (pofo_id, time, game_type, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                message = (f"Your time is: {total_time} seconds")
                print(f"Added SQL with no data in SQL: {total_time}s")
            
            # If the time_record exists
            else:
                # Call out the best time in SQL, using MIN() method of SQL
                best_time_held_db = db.execute("SELECT MIN(best_time) FROM profile WHERE pofo_id = ? AND game_type = ?", acc_id, number_L)
                best_time_held = float(best_time_held_db[0]["MIN(best_time)"])
                print(f"TYPE {type(best_time_held_db)}")
                print("best_time_held_db", best_time_held_db)
                print(f"Your time is: {total_time}")
                print(f"Best time found. Your best time in {number_L}: {best_time_held}")

                # Compare the best_time in SQL with the new total_time
                if best_time_held > total_time:
                    # INSERT a new data to db
                    db.execute("INSERT INTO profile (pofo_id, time, game_type, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                    message = (f"New Record! {total_time} seconds")
                    print(f"New record!!!!!! {total_time}s")
                else:
                    message = (f"Your time is: {total_time} seconds")
                    pass
            ############### SQL part ###############

            return jsonify({'endGame': message, 'js_display_number': number_R})                

        # else counter < 10: Keep running the game
        elif answer == guess and counter < 10:
            number_R = num_list[counter]
            answer = number_L * number_R
            counter += 1
            print("Counter: ", counter)
            # Refresh a new number to page
            return jsonify({'js_display_number': number_R})
       
        # if the guess is wrong, just lets user keep guessing
        else:
            print("Wrong: ", guess, "Answer: ", answer, "=", number_L, number_R)
            pass

    return render_template("game.html", jinja_username=username)


################################################# Advanced Game #################################################
@app.route('/advancedgame', methods=['GET', 'POST'])
@login_required
def game_advanced():

    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        random_list = random.sample(num_list, 9)

        global number_L
        global start_time
        global number_R
        global end_time
        global counter

        # Get number_L from form.js
        if request.args.get('number_L'):

            # If the user presses the refresh button in the middle of the game, it resets all Global value
            if start_time != 0 and number_R > 1:
                number_R = 1
                start_time = 0
                end_time = 0
                counter = 1
                number_L = int(request.args.get('number_L'))
                print("agame1")
                return jsonify({'js_number_L': number_L})
            # If not, normally to running the game
            else:
                number_L = int(request.args.get('number_L'))
                print("agame2")
                return jsonify({'js_number_L': number_L})


        # When user input a number and press Enter
        # Get guess from form.js
        if request.form.get('js_guess_adgame'):

            answer = number_L * number_R
            guess = int(request.form['js_guess_adgame'])

            # Save the start time when user input(and press Enter) first answer
            if counter == 1:
                start_time = time.time()
                print("2 START: ", start_time)

            # When the last answer is correct, Game End 
            if answer == guess and counter == 10:
                # Calculating Time
                end_time = time.time()
                print("END: ", end_time)
                total_time = float("{:.3f}".format((end_time - start_time)))
                print(f"time_lapsed:{end_time} - {start_time}")
                # Reset the Global values
                counter = 1
                number_R = 1
                date_time = datetime.now()
                print("Stopwatch: ", total_time)


                ############### SQL part ###############
                # SQL only save the best_time record when the current time faster than SQL's fastest record

                # Check if the best_time is exists in db or NOT
                data_check = db.execute("SELECT best_time FROM profile WHERE EXISTS(SELECT * FROM profile WHERE pofo_id = ? AND game_type = ?)", acc_id, number_L)
                # This is to check if data already exists. It will return [{'best_time': 4.441}, {'best_time': 9.717}]
                # So if it len(data_check) == 0, it means there is no data

                # If the best_time does NOT exist, use SQL INSERT to add a record
                if len(data_check) == 0:
                    db.execute("INSERT INTO profile (pofo_id, time, game_type, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                    print(f"Added SQL with no data in SQL: {total_time}s")
                
                # If the time_record exists
                else:
                    # Call out the best time in SQL, using MIN() method of SQL
                    best_time_held_db = db.execute("SELECT MIN(best_time) FROM profile WHERE pofo_id = ? AND game_type = ?", acc_id, number_L)
                    best_time_held = float(best_time_held_db[0]["MIN(best_time)"])
                    print(f"Your time is: {total_time}")
                    print(f"Best time found. Your best time in {number_L}: {best_time_held}")

                    # Compare the best_time in SQL with the new total_time
                    if best_time_held > total_time:
                        # INSERT a new data to db
                        db.execute("INSERT INTO profile (pofo_id, time, game_type, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                        print(f"New record!!!!!! {total_time}s")


                        # Show a game end message
                        message = (f"New record! {total_time} seconds")
                    else:
                        message = (f"Your time is: {total_time} seconds")
                        pass
                ############### SQL part ###############

                return jsonify({'endGame': message, 'js_display_number': number_R})                

            # else counter < 10: Keep running the game
            elif answer == guess and counter < 10:
                number_R = num_list[counter]
                answer = number_L * number_R
                counter += 1
                print("Counter: ", counter)
                # Refresh a new number to page
                return jsonify({'js_display_number': number_R})
        
            # if the guess is wrong, just lets user keep guessing
            else:
                print("Wrong: ", guess, "Answer: ", answer, "=", number_L, number_R)
                pass


        return render_template("advancedgame.html", jinja_username=username)
    else:
        return render_template("login.html")

################################################# CHANGE PASSWORD #################################################
@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change Password"""
    ########## Basic Checking ##########
    # Keep and Know who is logging in
    acc_id = session["user_id"]

    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]


        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":

            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            new_pw_confirmation = request.form.get("new_pw_confirmation")

            # Ensure username was submitted
            if not request.form.get("old_password"):
                return apology("must provide old password", 403)

            # Ensure password was submitted
            if not request.form.get("new_password"):
                return apology("must provide new password", 403)

            # Ensure password was submitted
            if not request.form.get("new_pw_confirmation"):
                return apology("must confirm password", 403)

            ########## Change Password Feature ##########
            # Query database
            rows = db.execute("SELECT * FROM users WHERE id = ?", acc_id)
            # [{'id': 9, 'username': 'j_01', 'hash': 'pbkdf2:sha256:260000$hrrWfY0MEkZRbZ5a$308f47d9d9268c3c4c9915eb747ec473c77dc9aa57b4a495ef7a66bf402208c7', 'cash': 10000}]

            if not check_password_hash(rows[0]["hash"], old_password):
                return apology("invalid old password", 403)

            if new_password != new_pw_confirmation:
                return apology("new password not match", 403)

            else:
                flash("Password Changed!")

                hash_password = generate_password_hash(new_password)

                db.execute("UPDATE users SET hash = ? WHERE id = ?", hash_password, acc_id)

                return render_template("changepasswordsuccess.html")

        return render_template("changepassword.html", jinja_username=username)
        # Ensure username exists and password is correct

    else:
        return render_template("login.html")


################################################# About #################################################
@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]


        return render_template("about.html", jinja_username=username)

    else:
        return render_template("login.html")

################################################# Basic Table #################################################
@app.route('/basic_table', methods=['GET', 'POST'])
@login_required
def basic_table():
    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]
        
        return render_template("basictable.html", jinja_username=username)
    else:
        return render_template("login.html")


################################################# Advanced Table #################################################
@app.route('/advanced_table', methods=['GET', 'POST'])
@login_required
def advanced_table():
    acc_id = session["user_id"]
    if acc_id != None:
        # Show user name on left bar
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]    

        return render_template("advancedtable.html", jinja_username=username)
    else:
        return render_template("login.html")




if __name__ == "__main__":
    app.run(debug=True)