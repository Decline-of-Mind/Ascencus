"""All Imports"""
import os
'''Imports MONGO_URI key and SECRECT_KEY'''
from os import path
if path.exists('env.py'):
    import env

from flask import Flask, render_template
import pymongo
from flask_pymongo import PyMongo

''' Initializes Flask application '''
app = Flask(__name__)

""" Setting up variables needed for Database """
MONGO_URI = os.environ.get('MONGO_URI')
DBS_NAME = 'Ascend'

app.config['MONGO_URI'] = MONGO_URI
app.config['MONGO_DBS'] = DBS_NAME

mongo= PyMongo(app)


@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html', movies=mongo.db.movies.find(), books=mongo.db.books.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')),
    debug=True)