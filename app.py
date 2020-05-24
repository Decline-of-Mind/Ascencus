""" All imports       """
import os

from os import path
if path.exists('env.py'):
    import env

from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
import pymongo
from flask_wtf import FlaskForm
from wtforms import Form, PasswordField, BooleanField, StringField, validators
from werkzeug.security import generate_password_hash, check_password_hash

""" Setting up flask app """
app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['MONGODB_NAME'] = 'Ascend'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


"""" defining Forms for WTForms """
class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class RegisterForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

""" First routing when entering website """
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        existing_user = users.find_one({'name' : form.username.data})

        if existing_user is None:
           hashed_pass = generate_password_hash(form.password.data)
           users.insert_one({'name': form.username.data , 'password': hashed_pass})
           session['username'] = form.username.data
           return redirect(url_for('index'))
        
        return "that username is already in use!"

    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
    port=int(os.environ.get('PORT', '5000')),
    debug=True)