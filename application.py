import os

import requests
from flask import Flask, session, render_template, url_for, request, session, redirect, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=["POST","GET"])
def signup():
    #function to create new users

    #checking request method
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':

        if request.form.get("username") is None or request.form.get("username")== '':
            flash("Username Required")
            return render_template("register.html")

        elif request.form.get("password") is None or request.form.get("password")=='' :
            flash("Password Required")
            return render_template("register.html")

        hash1 = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username , hash) VALUES(:username, :hash)",
                                  {"username": request.form.get("username"),
                                 "hash": hash1} )
        db.commit()


        user = db.execute("SELECT * FROM users WHERE username=:username", {"username": request.form.get("username")}).fetchone()
        db.commit()


        #if is None:
            #return apologyR("username is taken")

        session["user_id"] = user[0]

        return redirect(url_for("index"))

@app.route("/login", methods=["POST","GET"])
def login():
    #function to login

    if request.method == 'POST':

        if request.form.get("username") is None or request.form.get("username")=='':
            flash("Username Required")
            return render_template("login.html")

        elif request.form.get("password") is None or request.form.get("password")=='':
            flash("Password Required")
            return render_template("login.html")

        #checking if username is taken
        user = db.execute("SELECT * FROM users WHERE username=:username", {"username":request.form.get("username")}).fetchone()
        db.commit()


        if user is None:
            flash("User is Invalid")
            return render_template("login.html")

        #hash = generate_password_hash(request.form.get("password"))
        #print(user[2])
        #print(hash)
        password= request.form.get("password")
        log = check_password_hash(user[2],password)
        print(log)

        if log is not True:
            flash("Incorrect Password")
            return render_template("login.html")

        else:
            session["user_id"] = user[0]

        return redirect(url_for("index"))

    elif request.method == 'GET':
        return render_template('login.html')

@app.route("/logout")
def logout():
    #fucntion to logout
    session.clear()

    return redirect(url_for("index"))


@app.route("/search", methods=['POST','GET'])
@login_required
def search():

    if request.method == 'POST':


        val = request.form.get("value")
        val = '%' + val + '%'
        books = db.execute("SELECT * FROM books WHERE (title LIKE  :value OR author LIKE :value OR isbn LIKE :value ) ", {"value":val}).fetchall()
        db.commit()

        if books is None:
            flash("No Matches Found")
            return redirect(url_for("index"))

        return render_template("search.html", books=books)

    else:
        return redirect(url_for("index"))

@app.route("/<int:book_id>", methods=['POST','GET'])
@login_required
def display_b(book_id):

    book = db.execute("SELECT * FROM books WHERE bookid = :id",{"id": book_id}).fetchone()
    db.commit()

    isbn = book.isbn

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "j79IP84yXcyfsEu9Zu7p7Q", "isbns": isbn})
    response = res.json()

    reviews = db.execute("SELECT reviews.rating, reviews.comments, users.username  FROM reviews INNER JOIN users ON reviews.uid = users.userid WHERE bid = :id",{"id": book_id}).fetchall()
    db.commit()

    return render_template('book.html',book=book, reviews=reviews, response=response)

@app.route("/api/<string:isbn>", methods=['POST','GET'])
def book_api(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn": isbn}).fetchone()
    db.commit()

    book_id = book.bookid


    rates = db.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE bid = :id",{"id": book_id}).fetchone()
    db.commit()

    #since decimal point is not supported by json and normal float would cost unecessary bandwidth
    avg_s = round(float(rates[0]),3)

    print(rates)
    return jsonify({
                        "title": book.title,
                        "author": book.author,
                        "year": book.year,
                        "isbn": isbn,
                        "review_count":rates[1],
                        "average_score": avg_s
                    })


@app.route("/review/<int:book_id>", methods=['POST','GET'])
@login_required
def review(book_id):

    if request.method == 'POST':

        user_id = session["user_id"]

        x = db.execute(" SELECT * FROM reviews WHERE (uid = :uid AND bid = :bid) ", {"uid": user_id, "bid": book_id}).fetchone()

        if x is not None:
            flash("You have already reviewd this book and cannot review again.")


        else:
        #inserting data
            flag = db.execute("INSERT INTO reviews (uid, bid, rating, comments) VALUES (:uid, :bid, :rate, :comm)",
                                    {"uid": user_id, "bid": book_id, "rate":request.form.get("rating"), "comm":request.form.get("comments")})
            db.commit()

            if flag is None:
                print("insert quesry failed")


        book = db.execute("SELECT * FROM books WHERE bookid = :id",{"id": book_id}).fetchone()
        db.commit()

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "j79IP84yXcyfsEu9Zu7p7Q", "isbns": book.isbn})
        response = res.json()

        reviews = db.execute("SELECT reviews.rating, reviews.comments, users.username  FROM reviews INNER JOIN users ON reviews.uid = users.userid WHERE bid = :id",{"id": book_id}).fetchall()
        db.commit()

        return render_template('book.html',book=book, reviews=reviews, response=response)
