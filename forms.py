# forms.py
from wtforms import Form, StringField, SelectField
class SearchForm(Form):
    choices = [('artist', 'Artist'),
               ('album', 'Album'),
               ('movie', 'Movie'),
               ('actor', 'Actor'),
               ('director', 'Director'),
               ('track', 'Track')]
    select = SelectField('Search for:', choices=choices)
    search = StringField('')

#{{ render_field(form.artist) }}
class AlbumForm(Form):
    album_or_ep = [('0', 'Album'),
                   ('1', 'Ep')]
    id = StringField('Id')
    #artist = StringField('Artist')
    name = StringField('Album Title')
    releaseDate = StringField('Release Date')
    detailedInfo = StringField('Detailed Information')
    album_or_ep = SelectField('Album or Ep', choices=album_or_ep)