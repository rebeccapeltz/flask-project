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

#  save  sesssoin userid

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
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    #get username, password input and look up in db
    #if found set the sesssion[userid] = to id of user
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

