# main.py
from app import app, Album, Artist, Movie, Actor, Director, Track, db
from db_setup import init_db, db_session
from forms import SearchForm, AlbumForm
from flask import flash, render_template, request, redirect,session
from tables import Results, ResultsMov, ResultsArtist, ResultsDirector, ResultsActor, ResultsTrack

from flask_table import Table, Col, LinkCol


init_db()
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
    qry = Album.query.filter(Album.id==id)
    al = qry.first()
    if Album:
        form = AlbumForm(formdata=request.form, obj=al)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(al, form)
            flash('Album updated successfully!')
            return redirect('/Albuminfo')
        return render_template('edit_Album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    #</int:id>

@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    form = AlbumForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        al = Album()

        save_changes(al, form, new=True)
        flash('Album created successfully!')
        return redirect('/albuminfo')
    return render_template('new_album.html', form=form)

def save_changes(al, form, new=False):
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
    album_artists = form.album_artists.data ###NEED TO FIX RELATIONS!!!
    album_comment = form.album_comment.data
    album_rating = form.album_rating.data
    tracks = form.tracks.data
    if new:
        # Add the new album to the database
        db.session.add(al)
    # commit the data to the database
    db.session.commit()

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delet(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = Album.query.filter(Album.id==id)
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
#</int:id>

if __name__ == '__main__':
    app.run(debug=True)