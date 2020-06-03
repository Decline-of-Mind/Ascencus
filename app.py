"""All Imports"""
import os
'''Imports MONGO_URI key and SECRECT_KEY'''
from os import path
if path.exists('env.py'):
    import env

from flask import Flask, render_template, request, url_for, redirect
import pymongo
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

''' Initializes Flask application '''
app = Flask(__name__)

""" Setting up variables needed for Database """
MONGO_URI = os.environ.get('MONGO_URI')
DBS_NAME = 'Ascend'

app.config['MONGO_URI'] = MONGO_URI
app.config['MONGO_DBS'] = DBS_NAME

mongo= PyMongo(app)


@app.route('/')
def index():
    return render_template('base.html', movies=mongo.db.movies.find())

@app.route('/getmovies')
def get_movies():
    return render_template('getmovies.html', movies=mongo.db.movies.find())

@app.route('/getbooks')
def get_books():
    return render_template('getbooks.html', books=mongo.db.books.find())

@app.route('/full_movie/<movie_id>')
def full_movie(movie_id):
    return''

@app.route('/full_book/<book_id>')
def full_book(book_id):
    this_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('full_book.html', book = this_book)


@app.route('/addmovie', methods=['GET','POST'])
def add_movie():
    movie = mongo.db.movies
    movie.insert_one(request.form.to_dict())
    print(request.form.to_dict())
    return render_template('addmovie.html')

@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    return render_template('addbook.html')

@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    print(request.form.to_dict())
    return redirect(url_for('full_book'))




if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')),
    debug=True)