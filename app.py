"""All Imports"""
import os
'''Imports MONGO_URI key and SECRECT_KEY'''
from os import path
if path.exists('env.py'):
    import env

from flask import Flask, render_template, request, url_for, redirect, flash
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
    this_movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('full_movie.html', movie = this_movie)

@app.route('/full_book/<book_id>')
def full_book(book_id):
    this_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('full_book.html', book = this_book)


@app.route('/addmovie', methods=['GET', 'POST'])
def add_movie():
    return render_template('addmovie.html',
    movie=mongo.db.movies.find())

@app.route('/insert_movie', methods=['GET','POST'])
def insert_movie():
    movie = mongo.db.movies
    movie_id = movie.insert_one(request.form.to_dict()).inserted_id
    return redirect(url_for('full_movie', movie_id=movie_id))


@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    return render_template('addbook.html',
    book=mongo.db.books.find())

@app.route('/insert_book', methods=['GET','POST'])
def insert_book():
    book = mongo.db.books
    book_id = book.insert_one(request.form.to_dict()).inserted_id
    return redirect(url_for('full_book', book_id=book_id))

@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('editbook.html', book=the_book)

@app.route('/update_book/<book_id>')
def update_book(book_id):
    book = mongo.db.books
    book.update({'_id': ObjectId(book_id)},
    {
        'title': request.form.get('title'),
        'author': request.form.get('author'),
        'category': request.form.get('category'),
        'description': request.form.get('description'),
        'first_comment': request.form.get('first_comment'),
        'second_comment': request.form.get('second_comment'),
        'third_comment': request.form.get('third_comment'),
        'img_url': request.form.get('img_url'),
        'code': request.form.get('code')
    })

@app.route('/edit_movie/<movie_id>')
def edit_movie(movie_id):
    the_movie = mongo.db.books.find_one({'_id': ObjectId(movie_id)})
    return render_template('editmovie.html', movie=the_movie)

@app.route('/update_movie/<movie_id>')
def update_movie(movie_id):
    movie = mongo.db.movie
    movie.update({'_id': ObjectId(movie_id)},
    {
        'title': request.form.get('title'),
        'director': request.form.get('director'),
        'category': request.form.get('category'),
        'small_description': request.form.get('small_description'),
        'big_description': request.form.get('big_description'),
        'runtime': request.form.get('runtime'),
        'img_url': request.form.get('img_url'),
        'code': request.form.get('code')
    })

@app.route('/full_book/<book_id>')
def checkBookForEdit(book_id):
    inserted_code = request.form.get('insert_code')
    print(request.form)
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    if inserted_code == the_book.code:
        return render_template('editbook.html', book=the_book)
    else:
        flash('Your code is invalid')
        return render_template('full_book.html', book=the_book)


@app.route('/full_movie/<movie_id>', methods=['GET', 'POST'])
def checkMovieForEdit(movie_id):
    inserted_code = request.form.get("insert_code")
    the_movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    if inserted_code == the_movie.code:
        return render_template('editmovie.html', movie=the_movie)
    else:
        flash('Your code is invalid')
        return render_template('full_movie.html', movie=the_movie)










if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')),
    debug=True)