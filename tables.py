from flask_table import Table, Col, LinkCol
class Results(Table):
    id = Col('ID')
    cover = Col ('Cover' ) 
    name = Col('Album Name')
    album_or_ep = Col ('Album or EP')
    releaseDate= Col ('Release Date' )
    detailedInfo= Col ('Information')
    g_id= Col ('Genre')
    track_name= Col ('Track Names')
    c_id = Col ('Comments')
    artist = Col ('Artist')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delet = LinkCol('Delete', 'delet', url_kwargs=dict(id='id'))

class ResultsMov(Table):

    id = Col('Id')
    title = Col('Title')
    release_date = Col('Release Date')
    country = Col ('Country')
    detailed_information= Col ('Information')
    moviecomments  = Col('Comments')
    act = Col ('Actors')
    direct = Col('Directors')

class ResultsArtist(Table):

    id = Col('ID')
    name = Col('Name')
    portrait = Col ('Portrait')
    detailedInfo= Col ('Information')
    company = Col ('Company' )
    country = Col ('Country' )
    g_id= Col ('Genre')
    track_name= Col ('Track Names')
    album_id = Col ('Albums')

class ResultsDirector(Table):
    id = Col('ID')
    name = Col('Name')
    country = Col ('Country' )
    date_of_birth = Col ('Date Of Birth')
    direct = Col('Movies')

class ResultsActor(Table):
    id = Col('ID')
    name = Col('Name')
    country = Col ('Country' )
    date_of_birth = Col ('Date Of Birth')
    act = Col('Movies')

class ResultsTrack(Table):
    name = Col('Name')
    artist = Col('Artists')
    album = Col('Album')