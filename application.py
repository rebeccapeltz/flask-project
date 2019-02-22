import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)

@app.route("/logout", methods=["POST"])
def logout():
    #check for session[userid] and set to empty
    session["username"] = None
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    #allow a user to sign on and automatically sign off existing user
    #get username, password input and look up in db
    username = request.form.get("username")
    password = request.form.get("password")
    #some validation
    if len(username) == 0 or len (password) == 0:
      return render_template("error.html", message="Invalid Login (emtpy strings).")
    #if found set the sesssion[userid] = to id of user
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password":password}).rowcount == 1:
        session["username"] = username
    else:
        return render_template("error.html", message="Invalid Login (not registered).")
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    #get isbn, title, author and year and create a query
    books = []
    return render_template("books.html",books = books)

@app.route("/books/<int:book_id>")
def books(book_id):
   """Lists details about a single book."""
    #book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    #if book is None:
        #return render_template("error.html", message="No books found.")
    # get ratings
    # get goodreads ratings
    # Make sure book exists.
    #return render_template("book.html", book=book)

