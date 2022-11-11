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
# # Configure CS50 Library to use SQLite database
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


@app.route('/')
@login_required
def index():
    """Show profile page"""
    acc_id = session["user_id"]

    if acc_id != None:
        # Update current stocks price to update total value
        # Get the user data in db
        username_db = db.execute("SELECT username FROM users WHERE id = ?", acc_id)
        username = username_db[0]["username"]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(username)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")

    return render_template("layout.html", jinja_username=username)


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
            print("START: ", start_time)

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

            message = (f"Finished! \n Your time is: {total_time} seconds")
            date_time = datetime.now()
            print("Stopwatch: ", total_time)
            # Show a game end message and Reset the num_R to 1


            ############### SQL part ###############
            # SQL only save the best_time record when the current time faster than SQL's fastest record

            # Check if the best_time is exists in db or NOT
            data_check = db.execute("SELECT best_time FROM profile WHERE EXISTS(SELECT * FROM profile WHERE pofo_id = ? AND symbol = ?)", acc_id, number_L)
            # This is to check if data already exists. It will return [{'best_time': 4.441}, {'best_time': 9.717}]
            # So if it len(data_check) == 0, it means there is no data

            # If the best_time does NOT exist, use SQL INSERT to add a record
            if len(data_check) == 0:
                db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                print(f"Added SQL with no data in SQL: {total_time}s")
            
            # If the time_record exists
            else:
                # Call out the best time in SQL, using MIN() method of SQL
                best_time_held_db = db.execute("SELECT MIN(best_time) FROM profile WHERE pofo_id = ? AND symbol = ?", acc_id, number_L)
                best_time_held = float(best_time_held_db[0]["MIN(best_time)"])
                print(f"Your time is: {total_time}")
                print(f"Best time found. Your best time in {number_L}: {best_time_held}")

                # Compare the best_time in SQL with the new total_time
                if best_time_held > total_time:
                    # INSERT a new data to db
                    db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                    print(f"New record!!!!!! {total_time}s")
                    print("Added to SQL")
                else:
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

    return render_template("game.html")


################################################# Advanced Game #################################################
@app.route('/advancedgame', methods=['GET', 'POST'])
@login_required
def game_advanced():

    acc_id = session["user_id"]
    
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
            print("START: ", start_time)

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

            message = (f"Finished! \n Your time is: {total_time} seconds")
            date_time = datetime.now()
            print("Stopwatch: ", total_time)
            # Show a game end message and Reset the num_R to 1


            ############### SQL part ###############
            # SQL only save the best_time record when the current time faster than SQL's fastest record

            # Check if the best_time is exists in db or NOT
            data_check = db.execute("SELECT best_time FROM profile WHERE EXISTS(SELECT * FROM profile WHERE pofo_id = ? AND symbol = ?)", acc_id, number_L)
            # This is to check if data already exists. It will return [{'best_time': 4.441}, {'best_time': 9.717}]
            # So if it len(data_check) == 0, it means there is no data

            # If the best_time does NOT exist, use SQL INSERT to add a record
            if len(data_check) == 0:
                db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                print(f"Added SQL with no data in SQL: {total_time}s")
            
            # If the time_record exists
            else:
                # Call out the best time in SQL, using MIN() method of SQL
                best_time_held_db = db.execute("SELECT MIN(best_time) FROM profile WHERE pofo_id = ? AND symbol = ?", acc_id, number_L)
                best_time_held = float(best_time_held_db[0]["MIN(best_time)"])
                print(f"Your time is: {total_time}")
                print(f"Best time found. Your best time in {number_L}: {best_time_held}")

                # Compare the best_time in SQL with the new total_time
                if best_time_held > total_time:
                    # INSERT a new data to db
                    db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                    print(f"New record!!!!!! {total_time}s")
                    print("Added to SQL")
                else:
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

    return render_template("advancedgame.html")




################################################# Speed Run Game #################################################
@app.route('/speedrun', methods=['GET', 'POST'])
@login_required
def game_speedrun():

    acc_id = session["user_id"]
    
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
            print("START: ", start_time)

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

            message = (f"Finished! \n Your time is: {total_time} seconds")
            date_time = datetime.now()
            print("Stopwatch: ", total_time)
            # Show a game end message and Reset the num_R to 1


            ############### SQL part ###############
            # SQL only save the best_time record when the current time faster than SQL's fastest record

            # Check if the best_time is exists in db or NOT
            data_check = db.execute("SELECT best_time FROM profile WHERE EXISTS(SELECT * FROM profile WHERE pofo_id = ? AND symbol = ?)", acc_id, number_L)
            # This is to check if data already exists. It will return [{'best_time': 4.441}, {'best_time': 9.717}]
            # So if it len(data_check) == 0, it means there is no data

            # If the best_time does NOT exist, use SQL INSERT to add a record
            if len(data_check) == 0:
                db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                print(f"Added SQL with no data in SQL: {total_time}s")
            
            # If the time_record exists
            else:
                # Call out the best time in SQL, using MIN() method of SQL
                best_time_held_db = db.execute("SELECT MIN(best_time) FROM profile WHERE pofo_id = ? AND symbol = ?", acc_id, number_L)
                best_time_held = float(best_time_held_db[0]["MIN(best_time)"])
                print(f"Your time is: {total_time}")
                print(f"Best time found. Your best time in {number_L}: {best_time_held}")

                # Compare the best_time in SQL with the new total_time
                if best_time_held > total_time:
                    # INSERT a new data to db
                    db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                    print(f"New record!!!!!! {total_time}s")
                    print("Added to SQL")
                else:
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

    return render_template("speedrun.html")


################################################# Ultimate Speed Run Game #################################################
@app.route('/ultispeedrun', methods=['GET', 'POST'])
@login_required
def game_ultispeedrun():

    acc_id = session["user_id"]
    
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
            print("START: ", start_time)

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

            message = (f"Finished! \n Your time is: {total_time} seconds")
            date_time = datetime.now()
            print("Stopwatch: ", total_time)
            # Show a game end message and Reset the num_R to 1


            ############### SQL part ###############
            # SQL only save the best_time record when the current time faster than SQL's fastest record

            # Check if the best_time is exists in db or NOT
            data_check = db.execute("SELECT best_time FROM profile WHERE EXISTS(SELECT * FROM profile WHERE pofo_id = ? AND symbol = ?)", acc_id, number_L)
            # This is to check if data already exists. It will return [{'best_time': 4.441}, {'best_time': 9.717}]
            # So if it len(data_check) == 0, it means there is no data

            # If the best_time does NOT exist, use SQL INSERT to add a record
            if len(data_check) == 0:
                db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                print(f"Added SQL with no data in SQL: {total_time}s")
            
            # If the time_record exists
            else:
                # Call out the best time in SQL, using MIN() method of SQL
                best_time_held_db = db.execute("SELECT MIN(best_time) FROM profile WHERE pofo_id = ? AND symbol = ?", acc_id, number_L)
                best_time_held = float(best_time_held_db[0]["MIN(best_time)"])
                print(f"Your time is: {total_time}")
                print(f"Best time found. Your best time in {number_L}: {best_time_held}")

                # Compare the best_time in SQL with the new total_time
                if best_time_held > total_time:
                    # INSERT a new data to db
                    db.execute("INSERT INTO profile (pofo_id, time, symbol, best_time) VALUES (?, ?, ?, ?)", acc_id, date_time, number_L, total_time)
                    print(f"New record!!!!!! {total_time}s")
                    print("Added to SQL")
                else:
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

    return render_template("ultispeedrun.html")







if __name__ == "__main__":
    app.run(debug=True)