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

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        users = mongo.db.users
        users.find_one({'username': request.form['username']})
    return render_template('register.html')


MONGODB_URI =os.getenv("MONGO_URI")
DBS_NAME = os.getenv("MONGO_DBNAME")


if __name__ == '__main__':
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')),
    debug=True)
