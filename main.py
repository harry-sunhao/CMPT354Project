# main.py
from app import app, album, artist, movie, actor, director, track, db
from db_setup import init_db, db_session
from forms import SearchForm, AlbumForm
from flask import flash, render_template, request, redirect,session
from tables import Results, ResultsMov, ResultsArtist, ResultsDirector, ResultsActor, ResultsTrack
from db_creator import albums
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
        if search.data['select'] == 'album':
            qry = db_session.query(album).filter(
                album.name.contains(search_string))
            results = qry.all()
            table = Results(results)
        elif search.data['select'] == 'movie':
            qry = movie.query.filter(movie.title.contains(search_string))
            results = qry.all()
            table = ResultsMov(results)
        elif search.data['select'] == 'track':
            qry = album.query.filter(album.track_name.contains(search_string))
            results = qry.all()
            table = Results(results)
       # elif search.data['select'] == 'track':   #not needed
        #    qry = track.query.filter(track.name.contains(search_string))
        #    results = qry.all()
        #    table = ResultsTrack(results)
        elif search.data['select'] == 'artist':
            qry = artist.query.filter(artist.name.contains(search_string))
            results = qry.all()
            table = ResultsArtist(results)
        elif search.data['select'] == 'actor': 
            qry = actor.query.filter(actor.name.contains(search_string))
            results = qry.all()
            table = ResultsActor(results)
        elif search.data['select'] == 'director': #working
            qry = director.query.filter(director.name.contains(search_string))
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
 
    
@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    """
    Add a new album
    """
    form = AlbumForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        al = albums()

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
    #artist = artist()
    #artist.name = form.artist.data
    #album.artist = artist
    al.id = form.id.data
    al.cover = form.cover.data
    al.name = form.name.data
    al.releaseDate = form.releaseDate.data
    al.detailedInfo = form.detailedInfo.data
    al.album_or_ep = form.album_or_ep.data
    if new:
        # Add the new album to the database
        db.session.add(al)
    # commit the data to the database
    db.session.commit()

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = album.query.filter(album.id==id)
    al = qry.first()
    if album:
        form = AlbumForm(formdata=request.form, obj=al)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(al, form)
            flash('Album updated successfully!')
            return redirect('/albuminfo')
        return render_template('edit_album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    #</int:id>

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delet(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = album.query.filter(album.id==id)
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