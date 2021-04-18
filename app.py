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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/reratemm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'CMPT354PROJECT'
db = SQLAlchemy(app, use_native_unicode='utf8')

# relation
# many-Many relation for act
acts = db.Table('act',
                db.Column('movie_id', db.INTEGER(), db.ForeignKey('Movie.id'), primary_key=True),
                db.Column('actor_id', db.INTEGER(), db.ForeignKey('Actor.id'), primary_key=True)
                )
# many-Many relation for direct
directs = db.Table('direct',
                   db.Column('movie_id', db.INTEGER(), db.ForeignKey('Movie.id'), primary_key=True),
                   db.Column('director_id', db.INTEGER(), db.ForeignKey('Director.id'), primary_key=True)
                   )


# many-Many relation for produce
album_artists = db.Table('albumartist',
                         db.Column('album_id', db.INTEGER(), db.ForeignKey('Album.id'), primary_key=True),
                         db.Column('artist_id', db.INTEGER(), db.ForeignKey('Artist.id'), primary_key=True)
                         )

track_artists = db.Table('trackartist',
                         db.Column('track_id', db.INTEGER(), db.ForeignKey('Track.id'), primary_key=True),
                         db.Column('album_id', db.INTEGER(), db.ForeignKey('Album.id'), primary_key=True),
                         db.Column('artist_id', db.INTEGER(), db.ForeignKey('Artist.id'), primary_key=True)
                         )

# User part start
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login import UserMixin

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    email = db.Column('email', db.VARCHAR(255), unique=True)
    music_rating_weight = db.Column('music_rating_weight', db.FLOAT(255))
    movie_rating_weight = db.Column('movie_rating_weight', db.FLOAT(255))
    username = db.Column('username', db.VARCHAR(255), unique=True)
    password = db.Column('password', db.VARCHAR(255))
    certification_information = db.Column('certification_information', db.VARCHAR(255))
    movie_comment = db.relationship('Movie_Comment', back_populates="user")
    movie_rating = db.relationship('Movie_Rating', back_populates="user")
    album_comment = db.relationship('Album_Comment', back_populates="user")
    album_rating = db.relationship('Album_Rating', back_populates="user")
    track_rating = db.relationship('Track_Rating', back_populates="user")

    def validate_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        allUser = User.query.all()
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

        allUser = User.query.filter_by(username=username)
        print(allUser)
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
            if User.query.filter_by(email=email).first():
                flash("email is exist, please change another email.")
                return redirect(url_for('register'))
            user_ = User.query.first()
            if user_ is None:
                id = 1;
            else:
                id = len(User.query.all()) + 1
            t_user = User(id=id, email=email, username=username, password=password)
            db.session.add(t_user)
            db.session.commit()
            flash('Add user ' + request.form['username'] + ' successfully. ')
            return redirect(url_for('login'))
    return render_template('reg.html')


@app.route('/userinfo')
def show_all():
    a_user = User.query.all()
    return render_template('show_all.html', users=a_user)


@app.route('/user/delete/<int:user_id>', methods=['GET'])
@login_required
def delete(user_id):
    user_ = User.query.get_or_404(user_id)
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

    return render_template('home.html', user=username, login=isLogin)


# user part end


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    title = db.Column('title', db.VARCHAR(255))
    release_date = db.Column('release_date', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    detailed_information = db.Column('detailed_information', db.TEXT())
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('Genre.id'))
    acts = db.relationship('Actor', secondary=acts, lazy='subquery',
                           backref=db.backref('Movie', lazy=True))
    directs = db.relationship('Director', secondary=directs, lazy='subquery',
                              backref=db.backref('Movie', lazy=True))
    comment = db.relationship('Movie_Comment', back_populates='movie')
    rating = db.relationship('Movie_Rating', back_populates='movie')


class Movie_Comment(db.Model):
    __tablename__ = 'MovieComment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key=True, autoincrement=True)
    movie_id = db.Column('movie_id', db.INTEGER(), db.ForeignKey('Movie.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('User.id'))
    createtime = db.Column('createtime', db.DATETIME())
    content = db.Column('content', db.TEXT())
    user = db.relationship('User', back_populates='movie_comment', foreign_keys=[user_id])
    movie = db.relationship('Movie', back_populates='comment')
    
    def __init__(self, comment_id, movie_id, createtime, content):
        self.comment_id = comment_id
        self.movie_id = movie_id
        self.createtime = createtime
        self.content = content


class Movie_Rating(db.Model):
    __tablename__ = 'MovieRating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key=True, autoincrement=True)
    movie_id = db.Column('movie_id', db.INTEGER(), db.ForeignKey('Movie.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('User.id'))
    createtime = db.Column(db.DATETIME())
    value = db.Column('value', db.FLOAT())
    user = db.relationship('User', back_populates='movie_rating', foreign_keys=[user_id])
    movie = db.relationship('Movie', back_populates='rating')

    def __init__(self, rate_id, createtime, value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value


class Album(db.Model):
    __tablename__ = "Album"
    id = db.Column('id', db.INTEGER(), primary_key=True)
    cover = db.Column('cover', db.VARCHAR(255))
    name = db.Column('name', db.VARCHAR(255))
    album_or_ep = db.Column('album_or_ep', db.INTEGER())
    releaseDate = db.Column('releaseDate', db.DATETIME())
    detailedInfo = db.Column('detailedInfo', db.TEXT())
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('Genre.id'))
    album_artists = db.relationship('Artist', secondary=album_artists, lazy='subquery',
                                    backref=db.backref('Album', lazy=True))
    album_comment = db.relationship('Album_Comment', back_populates='album')
    album_rating = db.relationship('Album_Rating', back_populates='album')
    tracks = db.relationship('Track', backref='Album', lazy=True)
    
class Album_Comment(db.Model):
    __tablename__ = 'AlbumComment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key=True, autoincrement=True)
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey("Album.id"))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('User.id'))
    createtime = db.Column('createtime', db.DATETIME())
    content = db.Column('content', db.TEXT())
    user = db.relationship('User', back_populates='album_comment', foreign_keys=user_id)
    album = db.relationship('Album', back_populates='album_comment')

    def __init__(self, comment_id, createtime, content):
        self.comment_id = comment_id
        self.createtime = createtime
        self.content = content


class Album_Rating(db.Model):
    __tablename__ = 'AlbumRating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key=True, autoincrement=True)
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('Album.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('User.id'))
    createtime = db.Column(db.DATETIME())
    value = db.Column('value', db.FLOAT())
    user = db.relationship('User', back_populates='album_rating', foreign_keys=user_id)
    album = db.relationship('Album', back_populates='album_rating')
    
    def __init__(self, rate_id, createtime, value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value

class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    date_of_birth = db.Column('date_of_birth', db.VARCHAR(255))
    acts = db.relationship('Movie', secondary=acts, lazy='subquery',
                           backref=db.backref('Actor', lazy=True))


class Director(db.Model):
    __tablename__ = 'Director'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    date_of_birth = db.Column('date_of_birth', db.VARCHAR(255))
    directs = db.relationship('Movie', secondary=directs, lazy='subquery',
                              backref=db.backref('Director', lazy=True))

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_track_artist_movie = db.Column('album_track_artist_movie', db.INTEGER())
    artists = db.relationship('Artist', backref='Genre', lazy=True)
    albums = db.relationship('Album', backref='Genre', lazy=True)
    tracks = db.relationship('Track', backref='Genre', lazy=True)
    movies = db.relationship('Movie', backref='Genre', lazy=True)

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    portrait = db.Column('portrait', db.VARCHAR(255))
    detailedInfo = db.Column('detailedInfo', db.VARCHAR(255))
    company = db.Column('company', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('Genre.id'))
    album_artists = db.relationship('Album', secondary=album_artists, lazy='subquery',
                                    backref=db.backref('Artist', lazy=True))
    track_artists = db.relationship('Track', secondary=track_artists, lazy='subquery',
                                    backref=db.backref('Artist', lazy=True))

class Track_Rating(db.Model):
    __tablename__ = 'TrackRating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key=True)
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('Album.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('User.id'))
    createtime = db.Column(db.DATETIME())
    value = db.Column('value', db.FLOAT())
    user = db.relationship('User', back_populates='track_rating', foreign_keys=user_id)
    #track = db.relationship('Track', back_populates='ratings')

    def __init__(self, rate_id, createtime, value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value

class Track(db.Model):
    __tablename__ = 'Track'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('Album.id'), primary_key=True)
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('Genre.id'))
    track_artists = db.relationship('Artist', secondary=track_artists, lazy='subquery',
                                    backref=db.backref('Track', lazy=True))
    #ratings = db.relationship('Track_Rating', back_populates='tracks')

@app.route('/movie')
def mov():
    Movie.query.all()
    return render_template('movie.html', posts=Movie.query.all())


@app.route('/actorinfo')
def actors():
    return render_template('actors.html', actors=Actor.query.all())


@app.route('/albuminfo')
def albums():
    return render_template('album.html', albums=Album.query.all())


@app.route('/albumrate')
def albumcomments():
    return render_template('albumrate.html', albumcomments=album_comments.query.all())


@app.route('/artistinfo')
def artists():
    return render_template('artist.html', artists=Artist.query.all())

@app.route('/track')
def tracks():
    return render_template('track.html', tracks=Track.query.all())



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
