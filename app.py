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
class user(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    email = db.Column('email', db.VARCHAR(255),unique= True)
    music_rating_weight = db.Column(db.FLOAT(255))
    movie_rating_weight = db.Column(db.FLOAT(255))
    username = db.Column(db.VARCHAR(255))
    password = db.Column(db.VARCHAR(255))
    album_r_id = db.Column('album_r_id', db.INTEGER(), db.ForeignKey('albumrating.rate_id'))
    album_c_id = db.Column('album_c_id', db.INTEGER(), db.ForeignKey('albumcomment.comment_id'))
    track_r_id = db.Column('track_r_id', db.INTEGER(), db.ForeignKey('trackrating.rate_id'))
    movie_c_id = db.Column('movie_c_id', db.INTEGER(), db.ForeignKey('moviecomment.comment_id'))
    movie_r_id = db.Column('movie_r_id', db.INTEGER(), db.ForeignKey('movierating.rate_id'))
    certified_musician = db.Column(db.VARCHAR(255))

    def __init__(self, id,email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.music_rating_weight = 0
        self.movie_rating_weight = 0
        
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
act = db.Table('act',
    db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.INTEGER(), db.ForeignKey('actor.id'), primary_key=True)
)
#many-Many relation for direct
direct = db.Table('direct',
    db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
    db.Column('director_id', db.INTEGER(), db.ForeignKey('director.id'), primary_key=True)
)
class movie (db.Model):
    __tablename__ = 'movie'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    title = db.Column('title', db.VARCHAR(255))
    release_date = db.Column ('release_date', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    detailed_information = db.Column ('detailed_information', db.TEXT())
    moviecomments = db.relationship('moviecomment', backref='movie', lazy=True)
    act = db.relationship('actor', secondary=act, lazy='subquery',
        backref=db.backref('movie', lazy=True))
    direct = db.relationship('director', secondary=direct, lazy='subquery',
        backref=db.backref('movie', lazy=True))
    def __init__(self,id,title,release_date,country,detailed_information):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.country = country
        self.detailed_information = detailed_information

class moviecomment(db.Model):
    __tablename__ = 'moviecomment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key = True, autoincrement=True)
    movie_id = db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'))
    createtime = db.Column('createtime', db.DATETIME())
    content = db.Column ('content',db.TEXT())
    users= db.relationship('user', backref='moviecomment', lazy=True)
    def __init__(self,comment_id,movie_id,createtime,content):
        self.comment_id = comment_id
        self.movie_id = movie_id
        self.createtime = createtime
        self.content = content

class movierating(db.Model):
    __tablename__ = 'movierating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key = True)
    createtime = db.Column(db.DATETIME())
    value = db.Column ('value', db.FLOAT())
    users= db.relationship('user', backref='movierating', lazy=True)
    def __init__(self,rate_id,createtime,value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value

class actor (db.Model):
    __tablename__ = 'actor'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    date_of_birth = db.Column ('date_of_birth', db.VARCHAR(255))
    act = db.relationship('movie', secondary=act, lazy='subquery',
        backref=db.backref('actor', lazy=True))
    def __init__(self,id,name,country, date_of_birth):
        self.id = id
        self.name = name
        self.country = country
        self.date_of_birth = date_of_birth
#many-Many relation for produce
producealbum = db.Table('producealbum',
    db.Column('albumID', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True),
    db.Column('artistID', db.INTEGER(), db.ForeignKey('artist.id'), primary_key=True)
)

class album (db.Model):
    __tablename__ = 'album'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    cover = db.Column ('cover' ) 
    name = db.Column('name', db.VARCHAR(255))
    album_or_ep = db.Column ('album_or_ep', db.INTEGER())
    releaseDate= db.Column ('releaseDate', db.DATETIME() )
    detailedInfo= db.Column ('detailedInfo', db.TEXT())
    g_id= db.Column ('g_id', db.INTEGER(), db.ForeignKey('genre.id'))
    track_name= db.Column ('track_name', db.VARCHAR(255), db.ForeignKey('track.name'))
    c_id= db.Column ('c_id', db.INTEGER(), db.ForeignKey('albumcomment.comment_id'))
    artist= db.relationship('artist', backref='album', lazy=True)
    #producealbum = db.relationship('artist', secondary=producealbum, lazy='subquery',
        #backref=db.backref('album', lazy=True))
    def __init__(self,id,#cover,
            name,album_or_ep,releaseDate,detailedInfo):
            #,g_id,track_name,c_id):
        self.id = id
        #self.cover = cover
        self.name = name
        self.album_or_ep = album_or_ep
        self.releaseDate = releaseDate
        self.detailedInfo = detailedInfo
        #self.g_id = g_id
        #self.track_name = track_name
        #self.c_id = c_id

class artist (db.Model):
    __tablename__ = 'artist'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    portrait = db.Column ('portrait', db.VARCHAR(255)) 
    detailedInfo= db.Column ('detailedInfo', db.VARCHAR(255))
    company = db.Column ('company', db.VARCHAR(255))
    country= db.Column ('country', db.VARCHAR(255))
    g_id= db.Column ('g_id', db.INTEGER(), db.ForeignKey('genre.id'))
    track_name= db.Column ('track_name', db.VARCHAR(255),db.ForeignKey('track.name')
    )
    album_id= db.Column ('album_id', db.INTEGER(), db.ForeignKey('album.id')
    )
    #producealbum = db.relationship('album', secondary=producealbum, lazy='subquery',
    #    backref=db.backref('artist', lazy=True))
    
                
    def __init__(self,id,name,portrait,detailedInfo,company,country,g_id,track_name,album_id):
        self.id = id
        self.name = name
        self.portrait = portrait
        self.detailedInfo = detailedInfo
        self.company = company
        self.country = country
        self.g_id = g_id
        self.track_name = track_name
        self.album_id = album_id             

class albumartists(db.Model):
    __tablename__ = 'albumartists'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    artist = db.Column('artist', db.VARCHAR(255),primary_key=True)
    def __init__(self,id,artist):
        self.id = id
        self.artist= artist

class albumcomment(db.Model):
    __tablename__ = 'albumcomment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key = True)
    createtime = db.Column(db.DATETIME())
    content = db.Column ('content', db.INTEGER())
    album= db.relationship('album', backref='albumcomment', lazy=True)
    users= db.relationship('user', backref='albumcomment', lazy=True)
    def __init__(self,comment_id,createtime,content):
        self.comment_id = comment_id
        self.createtime = createtime
        self.content = content

class albumrating(db.Model):
    __tablename__ = 'albumrating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key = True)
    createtime = db.Column(db.DATETIME())
    value = db.Column ('value', db.FLOAT())
    users = db.relationship('user', backref='albumrating', lazy=True)
    def __init__(self,rate_id,createtime,value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value

class director(db.Model):
    __tablename__ = 'director'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    date_of_birth = db.Column ('date_of_birth', db.VARCHAR(255))
    direct = db.relationship('movie', secondary=direct, lazy='subquery',
        backref=db.backref('director', lazy=True))
    def __init__(self,id,name,country, date_of_birth):
        self.id = id
        self.name = name
        self.country = country
        self.date_of_birth = date_of_birth

class genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_track_artist_movie = db.Column ('album_track_artist_movie', db.VARCHAR(255))
    artist= db.relationship('artist', backref='genre', lazy=True)
    album= db.relationship('album', backref='genre', lazy=True)
    def __init__(self,id,name,country, date_of_birth,album_track_artist_movie):
        self.id = id
        self.name = name
        self.album_track_artist_movie = album_track_artist_movie

class track(db.Model):
    __tablename__ = 'track'
    name = db.Column('name', db.VARCHAR(255), primary_key=True)
    lyrics= db.Column ('lyrics', db.TEXT())
    artist = db.relationship('artist', backref='track', lazy=True)
    album= db.relationship('album', backref='track', lazy=True)
    def __init__(self,name,lyrics):
        self.id = id
        self.name = name
        self.lyrics = lyrics

class trackrating(db.Model):
    __tablename__ = 'trackrating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key = True)
    createtime = db.Column(db.DATETIME())
    value = db.Column ('value', db.FLOAT())
    users= db.relationship('user', backref='trackrating', lazy=True)
    def __init__(self,rate_id,createtime,value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value

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
