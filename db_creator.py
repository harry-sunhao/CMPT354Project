# db_creator.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('mysql+pymysql://root:123456@34.92.95.75:3306/ratemm', echo=True)
Base = declarative_base()
class artists(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "{}".format(self.name)
class albums(Base):
    """"""
    __tablename__ = "album"
    id = Column(Integer, primary_key=True)
    cover = Column (String) 
    name = Column(String)
    releaseDate = Column(String)
    detailedInfo = Column(String)
    album_or_ep = Column (Integer)
    #g_id= Column (Integer, ForeignKey('genre.id'))
    #track_name= Column (String, ForeignKey('track.name'))
    #c_id= Column ('c_id', db.INTEGER(), ForeignKey('albumcomment.comment_id'))

    #artist= relationship('artist', backref=backref(
     #   "album", order_by=id))

# create tables
Base.metadata.create_all(engine)