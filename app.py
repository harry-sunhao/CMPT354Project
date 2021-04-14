import os
import random

import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship, backref

from werkzeug.security import generate_password_hash, check_password_hash

from db_setup import db_session
from forms import SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://root:123456@34.92.95.75:3306/ratemm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'CMPT354PROJECT'
db = SQLAlchemy(app, use_native_unicode='utf8')

#User part start
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login import UserMixin
login_manager = LoginManager(app)
login_manager.login_view = 'login'
class User(db.Model,UserMixin):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    email = db.Column('email', db.VARCHAR(255), unique=True)
    music_rating_weight = db.Column('music_rating_weight', db.FLOAT(255))
    movie_rating_weight = db.Column('movie_rating_weight', db.FLOAT(255))
    username = db.Column('username', db.VARCHAR(255), unique=True)
    password = db.Column('password', db.VARCHAR(255))
    certification_information = db.Column('certification_information', db.VARCHAR(255))
    movie_comments = db.relationship('movie', secondary=movie_comments, lazy='subquery',
        backref=db.backref('user', lazy=True))
    movie_ratings = db.relationship('movie', secondary=movie_ratings, lazy='subquery',
        backref=db.backref('user', lazy=True))
    album_comments = db.relationship('album', secondary=album_comments, lazy='subquery',
        backref=db.backref('user', lazy=True))
    album_ratings = db.relationship('album', secondary=album_ratings, lazy='subquery',
        backref=db.backref('user', lazy=True))
    track_ratings = db.relationship('track', secondary=track_ratings, lazy='subquery',
        backref=db.backref('user', lazy=True))
        
    def validate_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    user_ = user.query.get(int(user_id))
    return user_

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        allUser = user.query.all()
        for user_ in allUser:
            if current_user.username == user_.username:
                user_.username = name
                db.session.commit()
                flash('Settings updated.')
                return redirect(url_for('index'))
    return render_template('setting.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        allUser = user.query.all()
        for user_ in allUser:
            if username == user_.username and user_.validate_password(password):
                login_user(user_)
                flash('Login success.')
                return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            email = request.form['email']
            if user.query.filter_by(email=email).first():
                flash("email is exist, please change another email.")
                return redirect(url_for('register'))
            user_ = user.query.first()
            if user_ is None:
                id = 1;
            else:
                id = len(user.query.all())+1
            t_user = user(id=id,email=email,username=username,password=password)
            db.session.add(t_user)
            db.session.commit()
            flash('Add user '+request.form['username']+' successfully. ')
            return redirect(url_for('login'))
    return render_template('reg.html')

@app.route('/userinfo')
@login_required
def show_all():
    a_user = user.query.all()
    return render_template('show_all.html', users=a_user)
@app.route('/user/delete/<int:user_id>', methods=['GET'])
@login_required
def delete(user_id):
    user_ = user.query.get_or_404(user_id)
    db.session.delete(user_)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@app.route('/')
def index():
    isLogin = False
    username = ""
    if 'username' in session:
        username = session['username']
        isLogin = True

    return render_template('home.html',user=username,login=isLogin)

#user part end




#many-Many relation for act
acts = db.Table('act',
    db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.INTEGER(), db.ForeignKey('actor.id'), primary_key=True)
)
#many-Many relation for direct
directs = db.Table('direct',
    db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
    db.Column('director_id', db.INTEGER(), db.ForeignKey('director.id'), primary_key=True)
)

movie_comments = db.Table('moviecomment',
    db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id')),
    db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id')),
    db.Column('comment_id', db.INTEGER(), primary_key = True, autoincrement=True),
    db.Column('createtime', db.DATETIME()),
    db.Column('content',db.TEXT())
)

movie_ratings = db.Table('movierating',
    db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
    db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'), primary_key=True),
    createtime = db.Column('createtime', db.DATETIME()),
    value = db.Column ('value', db.INTEGER())
)

class Movie (db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    title = db.Column('title', db.VARCHAR(255))
    release_date = db.Column ('release_date', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    detailed_information = db.Column ('detailed_information', db.TEXT())
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    acts = db.relationship('actor', secondary=acts, lazy='subquery',
        backref=db.backref('movie', lazy=True))
    directs = db.relationship('director', secondary=directs, lazy='subquery',
        backref=db.backref('movie', lazy=True))
    movie_comments = db.relationship('user', secondary=movie_comments, lazy='subquery',
        backref=db.backref('movie', lazy=True))
    movie_ratings = db.relationship('user', secondary=movie_ratings, lazy='subquery',
        backref=db.backref('movie', lazy=True))

class Actor (db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    date_of_birth = db.Column ('date_of_birth', db.VARCHAR(255))
    acts = db.relationship('movie', secondary=acts, lazy='subquery',
        backref=db.backref('actor', lazy=True))

class Director(db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    date_of_birth = db.Column ('date_of_birth', db.VARCHAR(255))
    directs = db.relationship('movie', secondary=directs, lazy='subquery',
        backref=db.backref('director', lazy=True))

#many-Many relation for produce
album_artists = db.Table('albumartist',
    db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True),
    db.Column('artist_id', db.INTEGER(), db.ForeignKey('artist.id'), primary_key=True)
)

album_comments = db.Table('albumcomment',
    db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id')),
    db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id')),
    db.Column('comment_id', db.INTEGER(), primary_key = True, autoincrement=True),
    db.Column('createtime', db.DATETIME()),
    db.Column ('content', db.TEXT())
)

album_ratings = db.Table('albumrating',
    db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key = True),
    db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'), primary_key = True),
    db.Column('createtime', db.DATETIME()),
    db.Column('value', db.INTEGER())
)

class Album (db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    cover = db.Column ('cover', db.VARCHAR(255))
    name = db.Column('name', db.VARCHAR(255))
    album_or_ep = db.Column ('album_or_ep', db.INTEGER())
    releaseDate= db.Column ('releaseDate', db.DATETIME() )
    detailedInfo= db.Column ('detailedInfo', db.TEXT())
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    album_artists = db.relationship('artist', secondary=album_artists, lazy='subquery',
        backref=db.backref('album', lazy=True))
    album_comments = db.relationship('user', secondary=album_comments, lazy='subquery',
        backref=db.backref('album', lazy=True))
    album_ratings = db.relationship('user', secondary=album_ratings, lazy='subquery',
        backref=db.backref('album', lazy=True))
    tracks = db.relationship('track', backref='album', lazy=True)

class Artist (db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    portrait = db.Column ('portrait', db.VARCHAR(255)) 
    detailedInfo = db.Column ('detailedInfo', db.VARCHAR(255))
    company = db.Column ('company', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    genre_id = db.Column ('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    album_artists = db.relationship('album', secondary=album_artists, lazy='subquery',
        backref=db.backref('artist', lazy=True))

class Genre(db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_track_artist_movie = db.Column ('album_track_artist_movie', db.INTEGER())
    artists = db.relationship('artist', backref='genre', lazy=True)
    albums = db.relationship('album', backref='genre', lazy=True)
    tracks = db.relationship('track', backref='genre', lazy=True)
    movies = db.relationship('movie', backref='genre', lazy=True)

track_artists = db.Table('trackartist',
    db.Column('track_id', db.INTEGER(), db.ForeignKey('track.id'), primary_key=True),
    db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True),
    db.Column('artist_id', db.INTEGER(), db.ForeignKey('artist.id'), primary_key=True)
)

track_ratings = db.Table('trackrating',
    db.Column('track_id', db.INTEGER(), db.ForeignKey('track.id'), primary_key=True),
    db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key = True),
    db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'), primary_key = True),
    db.Column('createtime', db.DATETIME()),
    db.Column('value', db.INTEGER())
)

class Track(db.Model):
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True)
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))

@app.route('/movie')
def mov():
    movie.query.all()
    return render_template('movie.html', posts = movie.query.all())

@app.route('/actorinfo')
def actors():
    return render_template('actors.html', actors=actor.query.all())

@app.route('/albuminfo')
def albums():
    return render_template('album.html', albums=album.query.all())

@app.route('/albumrate')
def albumcomments():
    return render_template('albumrate.html', albumcomments=albumcomment.query.all())

@app.route('/artistinfo')
def artists():
    return render_template('artist.html', artists=artist.query.all())

#add comment: works! no restrictions added yet for comment ID,(want to make it increment automatically but)
#and dont know how to get current time for createtime
@app.route('/addcom', methods=['GET', 'POST'])

def addcom(comment_id=None):
    if request.method == 'POST':
        if not request.form['comment_id'] or not request.form['movie_id'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            print(request.form['comment_id'], request.form['movie_id'], request.form['content'])
            #temp_comment_id = random.randint(1, 99999999999)
            createtime = str(datetime.now())
            moviecomments = moviecomment.query.all()

            t_mov = moviecomment(request.form['comment_id'], request.form['movie_id'], createtime, request.form['content'])
            db.session.add(t_mov)
            db.session.commit()
            flash('Add movie comment '+request.form['content']+' successfully. ')
            return redirect(url_for('mov'))
    return render_template('addcom.html')





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
