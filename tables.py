from flask_table import Table, Col, LinkCol
class Results(Table):
    id = Col('ID')
    cover = Col ('Cover' ) 
    name = Col('Album Name')
    genre_id = Col ('Genre')
    album_artists = Col ('Artists')
    album_comment = Col ('Comments')
    album_rating = Col ('Rating')
    tracks = Col ('Track Names')
    album_or_ep = Col ('Album or EP')
    releaseDate= Col ('Release Date' )
    detailedInfo= Col ('Information')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delet = LinkCol('Delete', 'delet', url_kwargs=dict(id='id'))

class ResultsMov(Table):
    id = Col('Id')
    title = Col('Title')
    release_date = Col('Release Date')
    country = Col ('Country')
    detailed_information= Col ('Information')
    genre_id = Col ('Genre')
    acts = Col ('Actors')
    directs = Col('Directors')
    comment = Col ('Comments')
    rating = Col ('Rating')
    
class ResultsArtist(Table):

    id = Col('ID')
    name = Col('Name')
    portrait = Col ('Portrait')
    detailedInfo= Col ('Information')
    company = Col ('Company' )
    country = Col ('Country' )
    genre_id = Col ('Genre')
    track_artists= Col ('Track Names')
    album_artists= Col ('Albums')

class ResultsDirector(Table):
    id = Col('ID')
    name = Col('Name')
    country = Col ('Country' )
    date_of_birth = Col ('Date Of Birth')
    directs = Col('Movies')

class ResultsActor(Table):
    id = Col('ID')
    name = Col('Name')
    country = Col ('Country' )
    date_of_birth = Col ('Date Of Birth')
    acts = Col('Movies')

class ResultsTrack(Table):
    id = Col('ID')
    name = Col('Name')
    album_id = Col('Album')
    genre_id = Col ('Genre')
    track_artists = Col ('Artist')