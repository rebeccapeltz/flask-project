import os

from flask import Flask, render_template, request, redirect, session, url_for,jsonify
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
    username = ""
    if (session['username'] != None):
       username = session['username']
    return render_template("index.html", username=username)

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)

@app.route("/logout", methods=["POST"])
def logout():
    #check for session[userid] and set to empty
    session["username"] = None
    return redirect(url_for('index'))

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
    return redirect(url_for('index'))


@app.route("/register", methods=["GET"])
def register():
  return render_template("register.html")

@app.route("/register_process", methods=["POST"])
def register_process():
    # get user name and password
    username = request.form.get("username")
    password = request.form.get("password")
    # check that user name not used and return error if used
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
        return render_template("error.html", message="Registration error (username exsits).")
  # insert username and password
    else:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
            {"username": username, "password":password})
        db.commit()
        # send to sucess
        return render_template("success.html", message="Registration success.")


@app.route("/search", methods=["POST"])
def search():
    #get isbn, title, authorand create a query
    isbn = request.form.get("isbn")
    author = request.form.get("author")
    title = request.form.get("title")

    query = f"SELECT * FROM books WHERE isbn LIKE \'%{isbn}%\' AND author LIKE \'%{author}%\' AND title LIKE \'%{title}%\'"
    app.logger.debug("QQQ:",query)
    books = db.execute(query,{"isbn": isbn, "author":author, "title":title}).fetchall()
    app.logger.debug("books length", len(books))
    return render_template("books.html",books = books)

@app.route("/books/<int:book_id>", methods=["GET"])
def books(book_id):
    app.logger.debug("book_id",book_id)
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    app.logger.debug("book", book)
    if book is None:
        return render_template("error.html", message="No books found.")
    # get ratings
    # get goodreads ratings
    # Make sure book exists.
    return render_template("book.html", book=book)

@app.route("/review", methods=["POST"])
def review():
  if 'username' not in session:
      return render_template("error.html", message="You must be logged in to use this feature (review).")
  #get book id, user id, rating, comments
  rating = request.form.get("rating")
  comments = request.form.get("comments")
  bookid = request.form.get("book_id")
  user = db.execute("SELECT * FROM users WHERE username = :username", {"username": session.get("username")}).fetchone()
  if user is None:
      return render_template("error.html", message="Can't find userid in reviews.")
  userid = user.id
  app.logger.debug("userid",user.id)
  
  # insert into review

  # send back to book
  # return redirect(url_for('index'),book, rating)
  return render_template("success.html", message="Review success.")

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    if 'username' not in session:
        return render_template("error.html", message="You must be logged in to use this feature (api/isbn).")
  
    app.logger.debug("isbn", isbn)
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    app.logger.debug("book", book)
    if book is None:
        return jsonify({"message": "book not found by isbn provided"}), 404

    book_dict =  {"title": book.title,
    "author": book.author,
    "year": book.year,
    "isbn": book.isbn,
    "review_count": 0,
    "average_score": 0.0}
    return jsonify(book_dict)


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
