# pReader
### Linux package file analyzer
### A preassignment for Reaktor job application

## About
This app is my solution to [Reaktors application preassignment](https://www.reaktor.com/junior-dev-assignment/).
In short, the app analyzes the */var/lib/dpkg/status* file found in Debian based Linux distributions, creating a HTML directory of the packages within for human friendly browsing.

The app was created with Pythons Flask framework and SQLAlchemy, with an SQLite3 database.
Due to the app being hosted on Heroku, the SQlite3 database is destroyed once every 24 hours.
That means all userdata is wiped from the server once per day. Convenient!


## Setup
To test the application locally, you should have python 3.x and pip installed.
I recommend you create a virtual environment for the apps extensions with:
```
pip install virtualenv
python -m venv venv
source venv/bin/activate
```

then clone the app into your local machine and install the required packages:
```
git clone https://github.com/jkerola/xxxxx.git
cd xxx
pip install -r requirements.txt
```

To run the pre-written unit tests:
```
pytest -s
```

To run the Flask development server:
```
python app.py
```
Then navigate to localhost:5000 in your browser.