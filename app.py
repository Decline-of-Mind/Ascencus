"""All Imports"""
import os
'''Imports MONGO_URI key and SECRECT_KEY'''
if os.path.exists('env.py'):
    import env

from flask import Flask, render_template, request, url_for, redirect, session, flash
import pymongo
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

''' Initializes Flask application '''
app = Flask(__name__)

""" Setting up variables needed for Database """
app.secret_key = os.environ.get('SECRET_KEY')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['MONGO_DBS'] = os.environ.get('DBS_NAME')

mongo= PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', movies=mongo.db.movies.find())


@app.route('/getbooks')
def get_books():
    return render_template('getbooks.html', books=mongo.db.books.find())


@app.route('/full_book/<book_id>', methods=['GET', 'POST'])
def full_book(book_id):
    print("hello")
    this_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('full_book.html', book = this_book)


'''Adding books | add_book is the html and form, insert_book the actual function that inserts'''

@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    return render_template('addbook.html',
    book=mongo.db.books.find(),
    categories=mongo.db.categories.find())


@app.route('/insert_book', methods=['GET','POST'])
def insert_book():
    book = mongo.db.books
    new_book = request.form.get("title")
    if book.count_documents({'title': new_book}, limit=1) == 0:
        book_id = book.insert_one(request.form.to_dict()).inserted_id
        ''''Returns the book that was just added'''
        return redirect(url_for('full_book', book_id=book_id))
    else:
        flash(u'Book already exists', 'info')
        return redirect(url_for('add_book'))


'''Editing books | Edit_book is the html and form, update_book the actual function that updates'''

@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('editbook.html', book=the_book,
    categories = mongo.db.categories.find())


@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    book = mongo.db.books
    updated_book = book.update({'_id': ObjectId(book_id)},
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
    return redirect(url_for('full_book', book_id=book_id))


'''Check whether the code inserted is equal to the database code'''

@app.route('/checkBookForEdit/<book_id>', methods=['POST'])
def checkBookForEdit(book_id):
    inserted_code = request.form.get('insert_code')
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    print(request.form)
    if inserted_code == the_book['code']:
        return render_template('editbook.html', book=the_book)
    else:
        flash(u'Your code is invalid', 'error')
        return render_template('full_book.html', book=the_book)

@app.route('/checkBookAndDelete/<book_id>', methods=['POST'])
def checkBookAndDelete(book_id):
    inserted_code = request.form.get('insert_deletecode')
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    print(request.form)
    print(inserted_code)
    print(the_book['code'])
    if inserted_code == the_book['code']:
        mongo.db.books.find_one_and_delete(({'_id': ObjectId(book_id)}))
        flash(u'Book has been Deleted', 'info')
        return redirect(url_for('get_books'))
    else:
        flash(u'Your code is invalid', 'error')
        return render_template('full_book.html', book=the_book)


"""MOVIES"""

@app.route('/getmovies')
def get_movies():
    return render_template('getmovies.html', movies=mongo.db.movies.find())


@app.route('/full_movie/<movie_id>' , methods=['GET', 'POST'])
def full_movie(movie_id):
    this_movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('full_movie.html', movie = this_movie)


'''Adding movies | add_movie is the html and form, insert_movie the actual function that inserts'''

@app.route('/addmovie', methods=['GET', 'POST'])
def add_movie():
    return render_template('addmovie.html',
    movie=mongo.db.movies.find(),
    categories=mongo.db.categories.find())


@app.route('/insert_movie', methods=['GET','POST'])
def insert_movie():
    movie = mongo.db.movies
    new_movie = request.form.get("title")
    if movie.count_documents({'title': new_movie}, limit=1) == 0:
        movie_id = movie.insert_one(request.form.to_dict()).inserted_id
    ''''Returns the movie that was just added'''
        return redirect(url_for('full_movie', movie_id=movie_id))
    else:
        flash(u'movie already exists', 'info')
        return redirect(url_for('add_movie'))

'''Editing movies | Edit_movie is the html and form, update_movie the actual function that updates'''

@app.route('/edit_movie/<movie_id>', methods=['POST'])
def edit_movie(movie_id):
    the_movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('editmovie.html', movie=the_movie,
    categories=mongo.db.categories.find())


@app.route('/update_movie/<movie_id>', methods=['POST'])
def update_movie(movie_id):
    movie = mongo.db.movies
    updated_movie = movie.update({'_id': ObjectId(movie_id)},
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
    return redirect(url_for('full_movie', movie_id=movie_id))

'''Check whether the code inserted is equal to the database code'''

@app.route('/checkMovieForEdit/<movie_id>', methods=['POST'])
def checkMovieForEdit(movie_id):
    inserted_code = request.form.get('insert_code')
    the_movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    print(request.form)
    print(inserted_code)
    print(the_movie['code'])
    if inserted_code == the_movie['code']:
        return render_template('editmovie.html', movie=the_movie,
        categories=mongo.db.categories.find())
    else:
        flash(u'Your code is invalid', 'error')
        return render_template('full_movie.html', movie=the_movie)


@app.route('/checkMovieAndDelete/<movie_id>', methods=['POST'])
def checkMovieAndDelete(movie_id):
    inserted_code = request.form.get('insert_deletecode')
    the_movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    print(request.form)
    if inserted_code == the_movie['code']:
        mongo.db.movies.find_one_and_delete(({'_id': ObjectId(movie_id)}))
        flash(u'Movie has been Deleted', 'info')
        return redirect(url_for('get_movies'))
    else:
        flash(u'Your code is invalid', 'error')
        return render_template('full_movie.html', movie=the_movie)








'''Application technical options'''
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')))