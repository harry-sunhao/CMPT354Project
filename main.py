# main.py
from app import app, album, artist, movie, actor, director, track
from db_setup import init_db, db_session
from forms import SearchForm, AlbumForm
from flask import flash, render_template, request, redirect
from tables import Results, ResultsMov, ResultsArtist, ResultsDirector, ResultsActor, ResultsTrack

init_db()
@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'album':
            qry = album.query.filter(album.name.contains(search_string))
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
            return redirect('/')
    else:
        flash('Please fill the fields')
        return redirect('/')

    if not results:
        flash('No results found wrong input!')
        return redirect('/')
    else:
        # display results

        table.border = True
        return render_template('results.html', table=table)

#@app.route('/albuminfo')
#def albums():
    #return render_template('album.html', albums=album.query.all())

if __name__ == '__main__':
    app.run()