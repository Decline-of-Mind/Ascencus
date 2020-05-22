import os

from os import path
if path.exists("env.py"):
    import env

from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('base.html')

@app.route('/register')
def register_user():
    return render_template('register.html')


MONGODB_URI =os.getenv("MONGO_URI")
DBS_NAME = os.getenv("MONGO_DBNAME")


if __name__ == '__main__':
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')),
    debug=True)

