import os
import random

import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship, backref

from werkzeug.security import generate_password_hash, check_password_hash

from db_setup import db_session
from forms import SearchForm, AlbumForm, MovieForm
from tables import Results, ResultsMov, ResultsTrack, ResultsArtist, ResultsActor, ResultsDirector

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/ratemm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@34.92.95.75:3306/ratemm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'CMPT354PROJECT'
db = SQLAlchemy(app, use_native_unicode='utf8')

# relation
# many-Many relation for act
acts = db.Table('act',
                db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
                db.Column('actor_id', db.INTEGER(), db.ForeignKey('actor.id'), primary_key=True)
                )
# many-Many relation for direct
directs = db.Table('direct',
                   db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'), primary_key=True),
                   db.Column('director_id', db.INTEGER(), db.ForeignKey('director.id'), primary_key=True)
                   )

# many-Many relation for produce
album_artists = db.Table('albumartist',
                         db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True),
                         db.Column('artist_id', db.INTEGER(), db.ForeignKey('artist.id'), primary_key=True)
                         )

track_artists = db.Table('trackartist',
                         db.Column('track_id', db.INTEGER(), db.ForeignKey('track.id'), primary_key=True),
                         db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True),
                         db.Column('artist_id', db.INTEGER(), db.ForeignKey('artist.id'), primary_key=True)
                         )

# User part start
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login import UserMixin

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    email = db.Column('email', db.VARCHAR(255), unique=True)
    music_rating_weight = db.Column('music_rating_weight', db.FLOAT(255))
    movie_rating_weight = db.Column('movie_rating_weight', db.FLOAT(255))
    username = db.Column('username', db.VARCHAR(255), unique=True)
    password = db.Column('password', db.VARCHAR(255))
    certification_information = db.Column('certification_information', db.VARCHAR(255))
    movie_comment = db.relationship('Movie_Comment', back_populates="user", cascade="all, delete-orphan")
    movie_rating = db.relationship('Movie_Rating', back_populates="user", cascade="all, delete-orphan")
    album_comment = db.relationship('Album_Comment', back_populates="user", cascade="all, delete-orphan")
    album_rating = db.relationship('Album_Rating', back_populates="user", cascade="all, delete-orphan")
    track_rating = db.relationship('Track_Rating', back_populates="user", cascade="all, delete-orphan")

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
    comments = Movie_Comment.query.filter_by(user_id=current_user.id).all()
    print(current_user.id)
    return render_template('setting.html',comments=comments)

@app.route('/delcom/<int:id>',methods=['GET'])
def delcom(id):
        mc = Movie_Comment.query.get_or_404(id)
        print(mc)
        db.session.delete(mc)
        db.session.commit()
        flash('Comment deleted.')
        return redirect(url_for('settings',comments=Movie_Comment.query.filter_by(user_id=current_user.id).all()))

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


def covertEpOrAlbum(lst, index):  # which one is album?
    for i in range(len(lst)):
        lst[i] = list(lst[i])
        if (lst[i][index] == 1):
            lst[i][index] = "Album"
        else:
            lst[i][index] = "EP"
    return lst


@app.route('/')
def index():
    movieNumber = Movie.query.count()
    albumNumber = Album.query.count()
    sql_query = "SELECT movie.id,movie.title,movie.country,movie.release_date FROM movie RIGHT JOIN( SELECT id FROM movie JOIN moviecomment WHERE moviecomment.movie_id = movie.id GROUP BY id ORDER BY count(*) DESC) AS pop ON movie.id = pop.id"
    moviePopular = list(db.session.execute(sql_query))
    sql_query = "SELECT data.id,data.name,data.album_or_ep,(genre.name) AS genreName FROM genre RIGHT JOIN(SELECT album.id,album.name,album.album_or_ep, album.genre_id FROM album RIGHT JOIN (SELECT id FROM album JOIN albumcomment WHERE albumcomment.album_id = album.id GROUP BY id ORDER BY count(*) DESC) AS pop ON album.id = pop.id) data ON data.genre_id=genre.id"
    albumPopular = list(db.session.execute(sql_query))
    albumPopular = covertEpOrAlbum(albumPopular, 2)
    # print(albumPopular)
    sql_query = "SELECT * FROM genre AS G WHERE NOT EXISTS(SELECT M.genre_id FROM movie AS M WHERE NOT EXISTS(SELECT * FROM genre AS G1 WHERE G1.name = G.name AND G1.id = M.genre_id ))"
    genreForAllMovies = list(db.session.execute(sql_query))
    return render_template('home.html', album_popular=albumPopular, movie_popular=moviePopular,
                           movie_number=movieNumber, album_number=albumNumber, genre_for_all_movies = genreForAllMovies)


# user part end


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    title = db.Column('title', db.VARCHAR(255))
    release_date = db.Column('release_date', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    detailed_information = db.Column('detailed_information', db.TEXT())
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    acts = db.relationship('Actor', secondary=acts, lazy='subquery',
                           backref=db.backref('Movie', lazy=True), cascade="all, delete")
    directs = db.relationship('Director', secondary=directs, lazy='subquery',
                              backref=db.backref('Movie', lazy=True), cascade="all, delete")
    comment = db.relationship('Movie_Comment', back_populates='movie', cascade="all, delete-orphan")
    rating = db.relationship('Movie_Rating', back_populates='movie', cascade="all, delete-orphan")


class Movie_Comment(db.Model):
    __tablename__ = 'moviecomment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key=True, autoincrement=True)
    movie_id = db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'))
    createtime = db.Column('createtime', db.DATETIME())
    content = db.Column('content', db.TEXT())
    user = db.relationship('User', back_populates='movie_comment', foreign_keys=[user_id])
    movie = db.relationship('Movie', back_populates='comment')

    def __init__(self, movie_id, user_id, createtime, content):
        self.movie_id = movie_id
        self.user_id = user_id
        self.createtime = createtime
        self.content = content


class Movie_Rating(db.Model):
    __tablename__ = 'movierating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key=True, autoincrement=True, nullable=False)
    movie_id = db.Column('movie_id', db.INTEGER(), db.ForeignKey('movie.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'))
    createtime = db.Column(db.DATETIME(), default=datetime.now())
    value = db.Column('value', db.FLOAT())
    user = db.relationship('User', back_populates='movie_rating', foreign_keys=[user_id])
    movie = db.relationship('Movie', back_populates='rating')

    def __init__(self,movie_id, user_id, value):
        self.value = value
        self.user_id = user_id
        self.movie_id = movie_id


class Album(db.Model):
    __tablename__ = "album"
    id = db.Column('id', db.INTEGER(), primary_key=True)
    cover = db.Column('cover', db.VARCHAR(255))
    name = db.Column('name', db.VARCHAR(255))
    album_or_ep = db.Column('album_or_ep', db.INTEGER())
    releaseDate = db.Column('releaseDate', db.DATETIME())
    detailedInfo = db.Column('detailedInfo', db.TEXT())
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    album_artists = db.relationship('Artist', secondary=album_artists, lazy='subquery',
                                    backref=db.backref('Album', lazy=True), cascade="all, delete")
    album_comment = db.relationship('Album_Comment', back_populates='album', cascade="all, delete-orphan")
    album_rating = db.relationship('Album_Rating', back_populates='album', cascade="all, delete-orphan")
    tracks = db.relationship('Track', backref='Album', lazy=True, cascade="all, delete-orphan")


class Album_Comment(db.Model):
    __tablename__ = 'albumcomment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key=True, autoincrement=True)
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey("album.id"))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'))
    createtime = db.Column('createtime', db.DATETIME())
    content = db.Column('content', db.TEXT())
    user = db.relationship('User', back_populates='album_comment', foreign_keys=user_id)
    album = db.relationship('Album', back_populates='album_comment')

    def __init__(self, comment_id, createtime, content):
        self.comment_id = comment_id
        self.createtime = createtime
        self.content = content


class Album_Rating(db.Model):
    __tablename__ = 'albumrating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key=True, autoincrement=True)
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'))
    createtime = db.Column(db.DATETIME())
    value = db.Column('value', db.FLOAT())
    user = db.relationship('User', back_populates='album_rating', foreign_keys=user_id)
    album = db.relationship('Album', back_populates='album_rating')

    def __init__(self, rate_id, createtime, value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    date_of_birth = db.Column('date_of_birth', db.VARCHAR(255))
    acts = db.relationship('Movie', secondary=acts, lazy='subquery',
                          backref=db.backref('Actor', lazy=True), cascade="all, delete")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    date_of_birth = db.Column('date_of_birth', db.VARCHAR(255))
    directs = db.relationship('Movie', secondary=directs, lazy='subquery',
                              backref=db.backref('Director', lazy=True), cascade="all, delete")


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_track_artist_movie = db.Column('album_track_artist_movie', db.INTEGER())
    artists = db.relationship('Artist', backref='Genre', lazy=True, cascade="all, delete-orphan")
    albums = db.relationship('Album', backref='Genre', lazy=True, cascade="all, delete-orphan")
    tracks = db.relationship('Track', backref='Genre', lazy=True, cascade="all, delete-orphan")
    movies = db.relationship('Movie', backref='Genre', lazy=True, cascade="all, delete-orphan")


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    portrait = db.Column('portrait', db.VARCHAR(255))
    detailedInfo = db.Column('detailedInfo', db.VARCHAR(255))
    company = db.Column('company', db.VARCHAR(255))
    country = db.Column('country', db.VARCHAR(255))
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    album_artists = db.relationship('Album', secondary=album_artists, lazy='subquery',
                                    backref=db.backref('Artist', lazy=True), cascade="all, delete")
    track_artists = db.relationship('Track', secondary=track_artists, lazy='subquery',
                                    backref=db.backref('Artist', lazy=True), cascade="all, delete")


class Track_Rating(db.Model):
    __tablename__ = 'trackrating'
    rate_id = db.Column('rate_id', db.INTEGER(), primary_key=True)
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'))
    user_id = db.Column('user_id', db.INTEGER(), db.ForeignKey('user.id'))
    createtime = db.Column(db.DATETIME())
    value = db.Column('value', db.FLOAT())
    user = db.relationship('User', back_populates='track_rating', foreign_keys=user_id, cascade="all, delete")

    # track = db.relationship('Track', back_populates='ratings')

    def __init__(self, rate_id, createtime, value):
        self.rate_id = rate_id
        self.createtime = createtime
        self.value = value


class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    name = db.Column('name', db.VARCHAR(255))
    album_id = db.Column('album_id', db.INTEGER(), db.ForeignKey('album.id'), primary_key=True)
    genre_id = db.Column('genre_id', db.INTEGER(), db.ForeignKey('genre.id'))
    track_artists = db.relationship('Artist', secondary=track_artists, lazy='subquery',
                                    backref=db.backref('Track', lazy=True), cascade="all, delete")
    # ratings = db.relationship('Track_Rating', back_populates='tracks')


@app.route('/movie')
def mov():

    return render_template('movie.html', movies=Movie.query.all())


@app.route('/movieinfo/<int:id>/',methods=['GET', 'POST'])
def movieinfo(id):
    movie = Movie.query.get_or_404(id)
    dirctors = movie.directs
    actors = movie.acts
    genre =Genre.query.get_or_404(movie.genre_id)
    comments =list(db.session.execute("SELECT DATE_FORMAT(moviecomment.createtime,'%Y-%m-%d')AS createtime,moviecomment.content,user.username FROM moviecomment JOIN user ON moviecomment.user_id = user.id AND moviecomment.movie_id = "+str(id)))
    rating = list(movie.rating)
    count = len(rating)
    sum = 0
    for rate in rating:
        sum += rate.value
    if count == 0:
        rating = 0
    else:
        rating = sum / count

    if request.method == 'POST':
        commentcontent = request.form['comment']
        print(commentcontent)
        return redirect('movieinfo.html', movie=movie, dirctors=dirctors, actors=actors, genre=genre,
                               comments=comments, rating=rating)

    return render_template('movieinfo.html', movie=movie, dirctors=dirctors,actors=actors,genre=genre,comments=comments,rating=rating )


@app.route('/actorinfo/<int:id>/')
def actors(id):
    actor = Actor.query.get_or_404(id)
    movies = actor.acts
    return render_template('actors.html', actor=actor,movies=movies)

@app.route('/director/<int:id>/')
def director(id):
    director = Director.query.get_or_404(id)
    movies = director.directs
    return render_template('director.html',director=director,movies=movies)
@app.route('/albuminfo')
def albums():
    return render_template('album.html', albums=Album.query.all())


@app.route('/artistinfo')
def artists():
    return render_template('artist.html', artists=Artist.query.all())


@app.route('/track')
def tracks():
    return render_template('track.html', tracks=Track.query.all())


# add comment: works! no restrictions added yet for comment ID,(want to make it increment automatically but)
# and dont know how to get current time for createtime

@app.route('/addcom/<int:id>/', methods=['GET', 'POST'])
@login_required
def addcom(id):
    if request.method == 'POST':
        if not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            createtime = str(datetime.now())
            user_id = current_user.id
            if db.session.query(Movie_Comment).filter(Movie_Comment.user_id==user_id,Movie_Comment.movie_id==id).all():
                flash("you already comment this movie.")
                return redirect(url_for('movieinfo',id=id))
            t_mov = Movie_Comment(id, user_id, createtime,
                                  request.form['content'])
            db.session.add(t_mov)
            db.session.commit()
            flash('Add movie comment ' + "\"" + request.form['content'] + "\"" + ' successfully. ')
            return redirect(url_for('movieinfo',id=id))
    return render_template('addcom.html')


@app.route('/addrate/<int:id>/', methods=['GET', 'POST'])
@login_required
def addrate(id):
    if request.method == 'POST':
        if not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            rate = int(request.form['content'])
            if (rate<1 or rate >10):
                flash('Please check your rate value', 'error')
                return redirect(url_for('addrate',id=id))
            user_id = current_user.id
            if db.session.query(Movie_Rating).filter(Movie_Rating.user_id==user_id,Movie_Rating.movie_id==id).all():
                flash("you already comment this movie.")
                return redirect(url_for('movieinfo',id=id))
            t_mov = Movie_Rating(id, user_id,request.form['content'])
            db.session.add(t_mov)
            db.session.commit()
            flash('Add movie rating ' + request.form['content'] + ' successfully. ')
            return redirect(url_for('movieinfo',id=id))
    return render_template('addrate.html',id=id)
# search part start
@app.route('/search', methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Album':
            qry = db_session.query(Album).filter(
                Album.name.contains(search_string))
            results = qry.all()
            table = Results(results)
        elif search.data['select'] == 'Movie':
            qry = Movie.query.filter(Movie.title.contains(search_string))
            results = qry.all()
            table = ResultsMov(results)
        elif search.data['select'] == 'Track':
            qry = Track.query.filter(Track.name.contains(search_string))
            results = qry.all()
            table = ResultsTrack(results)
        elif search.data['select'] == 'Track':
            qry = Track.query.filter(Track.name.contains(search_string))
            results = qry.all()
            table = ResultsTrack(results)
        elif search.data['select'] == 'Artist':
            qry = Artist.query.filter(Artist.name.contains(search_string))
            results = qry.all()
            table = ResultsArtist(results)
        elif search.data['select'] == 'Actor':
            qry = Actor.query.filter(Actor.name.contains(search_string))
            results = qry.all()
            table = ResultsActor(results)
        elif search.data['select'] == 'Director':
            qry = Director.query.filter(Director.name.contains(search_string))
            results = qry.all()
            table = ResultsDirector(results)
        else:
            flash('No results found!')
            return redirect('/search')
    else:
        flash('Please fill the fields')
        return redirect('/search')

    if not results:
        flash('No results found wrong input!')
        return redirect('/search')
    else:
        # display results
        table.border = True
        return render_template('results.html', table=table)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = Album.query.filter(Album.id == id)
    al = qry.first()
    if Album:
        form = AlbumForm(formdata=request.form, obj=al)
        if request.method == 'POST' and form.validate():
            # save edits
            album_save_changes(al, form)
            flash('Album updated successfully!')
            return redirect('/Albuminfo')
        return render_template('edit_Album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    # </int:id>


@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    form = AlbumForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        al = Album()

        album_save_changes(al, form, new=True)
        flash('Album created successfully!')
        return redirect('/albuminfo')
    return render_template('new_album.html', form=form)

@app.route('/new_movie', methods=['GET', 'POST'])
def new_movie():
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        movie_created = Movie()

        movie_save_changes(movie_created, form, new=True)
        flash('Movie created successfully!')
        return redirect('/movie')
    return render_template('new_movie.html', form=form)

def album_save_changes(al, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    al.id = form.id.data
    al.cover = form.cover.data
    al.name = form.name.data
    al.releaseDate = form.releaseDate.data
    al.detailedInfo = form.detailedInfo.data
    al.album_or_ep = form.album_or_ep.data
    genre_id = form.genre_id.data
    album_artists = form.album_artists.data  ###NEED TO FIX RELATIONS!!!
    album_comment = form.album_comment.data
    album_rating = form.album_rating.data
    tracks = form.tracks.data
    if new:
        # Add the new album to the database
        db.session.add(al)
    # commit the data to the database
    db.session.commit()

def movie_save_changes(mov, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    mov.id = form.id.data
    mov.title = form.title.data
    mov.release_date = form.release_date.data
    mov.country = form.country.data
    mov.detailed_information = form.detailed_information.data
    mov.genre_id = form.genre_id.data
    if new:
        # Add the new album to the database
        db.session.add(mov)
    # commit the data to the database
    db.session.commit()

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delet(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = Album.query.filter(Album.id == id)
    al = qry.first()
    if al:
        form = AlbumForm(formdata=request.form, obj=al)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db.session.delete(al)
            db.session.commit()
            flash('Album deleted successfully!')
            return redirect('/albuminfo')
        return render_template('delete_album.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


# search part end

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
