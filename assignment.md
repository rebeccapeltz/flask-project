## Assignment

### Heroku
1. Navigate to https://www.heroku.com/, and create an account if you don’t already have one.
1. On Heroku’s Dashboard, click “New” and choose “Create new app.”
Give your app a name, and click “Create app.”
1. On your app’s “Overview” page, click the “Configure Add-ons” button.
1. In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
1. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision.”
1. Now, click the “Heroku Postgres :: Database” link.
You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database. You can access the database via Adminer, filling in the server (the “Host” in the credentials list), your username (the “User”), your password, and the name of the database, all of which you can find on the Heroku credentials page.



1. Clone your username/project1-username repository from GitHub (note: this is NOT your web50/project1-username repository).
1. In a terminal window, navigate into your project1 directory.
Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary Python packages (Flask and SQLAlchemy, for instance) are installed.
1. Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py. You may optionally want to set the environment variable FLASK_DEBUG to 1, which will activate Flask’s debugger and will automatically reload your web application whenever you save a change to a file.
1. Set the environment variable DATABASE_URL to be the URI of your database, which you should be able to see from the credentials page on Heroku.
1. Run flask run to start up your Flask application.
1. If you navigate to the URL provided by flask, you should see the text "Project 1: TODO"!