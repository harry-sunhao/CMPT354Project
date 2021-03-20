import os
import random

import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/reratemm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app, use_native_unicode='utf8')


class user(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    email = db.Column('email', db.VARCHAR(255), primary_key=True)
    music_rating_weight = db.Column(db.FLOAT(255))
    movie_rating_weight = db.Column(db.FLOAT(255))
    username = db.Column(db.VARCHAR(255))
    password = db.Column(db.VARCHAR(255))
    album_r_id = db.Column(db.INTEGER())
    album_c_id = db.Column(db.INTEGER())
    track_r_id = db.Column(db.INTEGER())
    movie_c_id = db.Column(db.INTEGER())
    movie_r_id = db.Column(db.INTEGER())
    certified_musician = db.Column(db.VARCHAR(255))

    def __init__(self, id, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.id = id
        self.music_rating_weight = 0
        self.movie_rating_weight = 0

class movie (db.Model):
    __tablename__ = 'movie'
    id = db.Column('id', db.INTEGER(), primary_key=True)
    title = db.Column('title', db.VARCHAR(255))
    release_date = db.Column ('release_date', db.VARCHAR(255))
    country = db.Column ('country', db.VARCHAR(255))
    detailed_information = ('detailed_information', db.TEXT)
    def __init__(self,id,title,release_date,country,detailed_information):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.country = country
        self.detailed_information = detailed_information

class moviecomment(db.Model):
    __tablename__ = 'moviecomment'
    comment_id = db.Column('comment_id', db.INTEGER(), primary_key = True)
    movie_id = db.Column('movie_id', db.INTEGER(), primary_key = True)
    createtime = db.Column(db.DATETIME)
    content = db.Column (db.TEXT)

    def __init__(self,comment_id,movie_id,createtime,content):
        self.comment_id = comment_id
        self.movie_id = movie_id
        self.createtime = createtime
        self.content = content

@app.route('/')
def showmovie():
    return render_template('home.html', posts=movie.query.all())


@app.route('/userinfo')
def show_all():
    a_user = user.query.all()
    return render_template('show_all.html', users=a_user)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            print(request.form['username'], request.form['password'], request.form['email'])
            temp_id = random.randint(1, 99999999999)
            users = user.query.all()

            isContain = 0
            while (isContain == 0):
                for temp in users:
                    print(temp.id,temp.username,temp.email)
                    if (temp.id == temp_id):
                        temp_id = random.randint(1, 9999999)
                        isContain = 0
                        break
                    if (temp.username == request.form['username']):
                        flash('username is exist, please change it.')
                        return render_template('reg.html')
                    if (temp.email == request.form['email']):
                        flash('email is exist, please change it.')
                        return render_template('reg.html')

                else:
                    isContain = 1
            t_user = user(temp_id, request.form['email'], request.form['username'], request.form['password'])
            db.session.add(t_user)
            db.session.commit()
            flash('Add user '+request.form['username']+' successfully. ')
            return redirect(url_for('show_all'))
    return render_template('reg.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
