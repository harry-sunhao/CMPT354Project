# forms.py
from wtforms import Form, StringField, SelectField, DateField, IntegerField
class SearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Movie', 'Movie'),
               ('Actor', 'Actor'),
               ('Director', 'Director'),
               ('Track', 'Track')]
    select = SelectField('Search for:', choices=choices)
    search = StringField('')


class AlbumForm(Form):
    album_or_ep = [('0', 'Album'),
                   ('1', 'Ep')]
    genre_id = [('1', 'Genre 1'),
                ('2', 'Genre 2'),
                ('3', 'Genre 3'),
                ('4', 'Genre 4'),
                ('5', 'Genre 5')]
    album_rating = [('1', '1'),
                    ('2', '2'),
                    ('3', '3'),
                    ('4', '4'),
                    ('5', '5'),
                    ('6', '6'),
                    ('7', '7'),
                    ('8', '8'),
                    ('9', '9'),
                    ('10', '10')]
    id = IntegerField('Id')
    cover = StringField('Cover')
    name = StringField('Name')
    album_or_ep = SelectField('Album or Ep', choices=album_or_ep)
    releaseDate = DateField('Release Date (FORMAT: YYYY-MM-DD)')
    detailedInfo = StringField('Detailed Information')
    genre_id = SelectField('Genre', choices=genre_id)
    album_artists = StringField('Artists')
    album_comment = StringField('Comments')
    album_rating = SelectField('Rating', choices=album_rating)
    tracks = StringField('Tracks') #needs to make sure relation works
