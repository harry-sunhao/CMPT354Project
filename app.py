import os
import random
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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/userinfo')
def show_all():
    return render_template('show_all.html', users=user.query.all())


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
            while (isContain != 0):
                for temp in users:
                    if (temp.id == temp_id):
                        temp_id = random.randint(1, 9999999)
                        isContain = 0
                        break
                else:
                    isContain = 1
            t_user = user(temp_id, request.form['email'], request.form['username'], request.form['password'])
            db.session.add(t_user)
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('reg.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
