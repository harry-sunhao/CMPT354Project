# forms.py
from wtforms import Form, StringField, SelectField
class SearchForm(Form):
    choices = [('Artist', 'artist'),
               ('Album', 'album'),
               ('Movie', 'movie'),
               ('Actor', 'actor'),
               ('Director', 'director'),
               ('Track', 'track')]
    select = SelectField('Search for:', choices=choices)
    search = StringField('')

