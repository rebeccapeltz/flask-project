# Project 1

## Web Programming with Python and JavaScript

### Tables created for PostgreSQL
*books*
```
CREATE TABLE books (
 id SERIAL PRIMARY KEY,
 isbn VARCHAR NOT NULL,
 title VARCHAR NOT NULL,
 author VARCHAR NOT NULL,
 year INTEGER NOT NULL
); 
```
*reviews* 
```
CREATE TABLE reviews (
 id SERIAL PRIMARY KEY,
 book_id INTEGER REFERENCES books (id),
 user_id INTEGER REFERENCES users (id),
 comments VARCHAR,
 rating INTEGER,
 CHECK (rating > 0),
 CHECK (rating < 6)
);
```
*users* 
```
CREATE TABLE users (
 id SERIAL PRIMARY KEY,
 username VARCHAR NOT NULL,
 password VARCHAR NOT NULL
); 
```
###
Routes
`/`
This shows a login form and a register link if not logged in
Once user is logged in a search form is revealed and user can do wild card search on an variable
If data is found the user is routed to books
Also submits a logout if a user is logged in and clicks on logout

`/register`  
This allows user to register with email and password and takes user back to home

`/search`  
Process the search inputs and send to books page

`/review`  
Process the review form and rerender the book.html page

`/books/ISBN`  
Process link to a single book and send to book.html page (NOTE: with more time I would have liked to move /reveiw code into /books/ISBN and have it process GET and POST)

`/api/ISBN`  
Looks up ISBN and returns data collected by app in json format if found or a 404 status code if not found

## Pages

`index.html`  
render the login and logout 

`book.html` 
If user clicks on a book link they are shown an individual book with ratings from good reads and what ever has been collected in the app.  

There is also form where the user can provide a rating and commments.  The user can't enter more than one comment about the book, but they can update their rating and comments.

`books.html`  
A place to list books found in search

`register.html`  
A registration form
 
`404.html`    
A place for unfound pages


`success.html`
There is a success page mostly used in development while working on queries.

`/error`
There is an error page for errors with messages

### NOTES:
I would have liked to do some refactoring and styling but didn't have enough time.  I could have added some more message about book not found or ratings not found.




### Requirements  

1. Registration: Users should be able to register for your website, providing (at minimum) a username and password.
1. Login: Users, once registered, should be able to log in to your website with their username and password.
1. Logout: Logged in users should be able to log out of the site.
1. Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN nubmer, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
1. Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
1. Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
1. Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
1. Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
1. API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
1. If the requested ISBN number isn’t in your database, your website should return a 404 error.

You should be using raw SQL commands (as via SQLAlchemy’s execute method) in order to make database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.
In README.md, include a short writeup describing your project, what’s contained in each file, a list of all of the tables in your database and what column names (and data types) are in each column, and (optionally) any other additional information the staff should know about your project.
1. If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!
