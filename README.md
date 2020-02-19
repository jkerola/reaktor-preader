# pReader
#### Linux package file analyzer; preassignment for Reaktor job application
#### [View pReader at jkerola-preader.herokuapp.com](http://jkerola-preader.herokuapp.com)

## About
pReader (package-reader) is my solution to [Reaktors application preassignment](https://www.reaktor.com/junior-dev-assignment/).

In short, the app analyzes the */var/lib/dpkg/**status*** file found in Debian based Linux distributions, creating a HTML directory of the packages within for human friendly browsing.

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
git clone https://github.com/jkerola/reaktor-preader.git
cd reaktor-preader
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
Two example files are provided in the ***example_files*** directory:

***status.real*** is data provided by [Reaktors Lauri Piispanen](https://gist.github.com/lauripiispanen/29735158335170c27297422a22b48caa)

***status.raspberry*** is real data from a Raspberry pi running RaspianOS

#### If you have any questions, feel free to message me!
