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
    if (session.get('username') != None):
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
     # Make sure book exists.
    if book is None:
        return render_template("error.html", message="No books found (books/book_id).")
    # get user
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": session.get("username")}).fetchone()
    if user is None:
        return render_template("error.html", message="No user found (books/book_id).")
    # get review
    review = db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id=:user_id", 
        {"book_id": book.id,"user_id":user.id}).fetchone()
    # get goodreads ratings
   
    return render_template("book.html", book=book, review=review)

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
      return render_template("error.html", message="Can't find userid to post review.")
  userid = user.id
  app.logger.debug("userid",user.id)
  # does review exist
  review = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id= :book_id", {"user_id": userid, "book_id":bookid}).fetchone()
  if review is None:
      # insert into review
      db.execute("INSERT INTO reviews (book_id, user_id, comments, rating) VALUES (:book_id, :user_id, :comments, :rating)", 
            {"book_id": bookid, "user_id":userid, "comments":comments, "rating":rating})
      db.commit()
  else:
      #update
      db.execute("UPDATE reviews SET rating = :rating, comments = :comments WHERE user_id = :user_id AND book_id= :book_id",
       {"user_id": userid, "book_id":bookid,"rating": rating, "comments":comments})
      db.commit()
  
  # send back to book
  # return redirect(url_for('index'),book, rating)
  # return render_template("success.html", message="Review success.")

  # get book and review and send back to book
  book = db.execute("SELECT * FROM books WHERE id = :bookid", {"bookid": bookid}).fetchone()
  review = db.execute("SELECT rating, comments FROM reviews WHERE book_id = :book_id AND user_id = :user_id", {"book_id": bookid,"user_id":userid}).fetchone()
  reviewAgg = db.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE book_id = :book_id GROUP BY book_id", {"book_id": bookid}).fetchone()

  return render_template("book.html", book=book, review=review, reviewAgg=reviewAgg)


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
