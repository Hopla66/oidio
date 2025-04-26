import hashlib
import os


def create_ID( artist:str, album:str='')->str:
  """ Creates a unique ID for an artist or for an album """
  res = hashlib.md5( (artist+album).encode()).hexdigest()
  return res
 
class Artist:
  def __init__(self):
    pass
    
class Album:
  def __init__(self):
    pass    


class Track(object):
  """ Track of an Album."""
  def __init__( self, name:str, tracknumber:str, length:str, file:str, album:Album=None):
    self.name:str = name
    self.tracknumber:str = tracknumber
    self.length:str = length
    self._album:Album = album
    self.file:str = file

  @property
  def album(self)->Album:
    return self._album

  @album.setter
  def album( self, value):
    self._album = value

  def list( self):
    print("    . {0} - {1} - {2} | {3} ".format(self.name, self.tracknumber, self.length, self.file))

  def __str__(self):
    return "<Track "+self.name+">"


class Album(object):
  """ Album of an Artist."""
  def __init__( self, name:str, year:str, genre:str, artist:Artist=None, tracks:list[Track]=None, id:str=""):
    self.name:str = name
    self.year:str = year
    self.genre:str = genre
    self._artist:Artist = artist
    self.cover:str = ""
    self.folder:str = ""
    self.tracks:list[Track] = []

    if tracks is not None and len(tracks) > 0:
      self.tracks = tracks
      self.folder = os.path.dirname( tracks[0].file)
    self.id:str = create_ID( name)

  def add_track( self, track:Track)->Track:
    """ Adds a Track to this Album, if the Track doesn't exist yet"""
    t:Track = self.get_track( track.name)
    if t is None:
      self.tracks.append(track)
      track.album = self
      self.folder =os.path.dirname( track.file)
      #self.write_coverart()
      return track
    else:
      return t

  def get_track( self, trackName:str)->Track:
    for t in self.tracks:
      if( t.name == trackName):
        return t
    return None
  
  def check( self):
    for t in self.tracks:
      t.album = self

  def list( self):
    print( "  - Album: {0} - {1} genre {2}".format( self.name, self.year, self.genre)) 
    for t in self.tracks:
      t.list()    

  @property
  def artist( self):
    return self._artist

  @artist.setter
  def artist(self,value:Artist):
    self._artist = value
    self.id = create_ID( value.name, self.name)


  def __str__(self):
    return "<Album "+self.name+">"

#
#
class Artist(object):
  def __init__( self, name:str, id:str='', albums:list[Album]=None):

    self.albums:list[Album] = [] if albums is None else albums
    self.name:str = name
    self.id:str = create_ID( name)

  def add_album( self, album:Album)->Album:
    a:Album = self.get_album(album.name)
    if a is None:
      a = album
      self.albums.append( a)
      a.artist = self
    return a
  
  def get_album( self, albumName:str)->Album:
    for a in self.albums:
      if a.name == albumName:
        return a
    return None
  
  def check( self):
    for a in self.albums:
      a.artist = self
      a.check()

  def list( self):
    print( "Artist: {0}  #albums: {1}".format(self.name, len(self.albums)))
    for a in self.albums:
      a.list()

  def __str__(self):
    return "<Artist "+self.name+" "+str(len(self.albums))+">"


class Artists(dict):
  """ Store of all Artists with their Albums and Tracks."""

  def add( self, a:Artist):
    """ Adds an Artist to the store, if it doesn't exist yet"""
    self.update( {a.name: a})

  def add_artist( self, name:str):
    """ Creates a new Artist and adds it to the store if it doesn't exist yet. Returns the Artist."""
    item:Artist = self.get(name) 
    if( item is None):
      a = Artist( name)
      self.add( a)
      return a
    else:
      return item

  def add_album( self, artist, albumName, year, genre)->Album:
    """ Adds an Album to the store, if this Album doesn't exist yet. If the Album's Artist doesn't exist yet in the model, it is added. 
        Returns the Album.
    """
    a = self.add_artist( artist)
    album = Album( albumName, year, genre)
    album = a.add_album( album)
    return album
  
  def add_track( self, file:str, name:str, tracknumber:str, length:str, artist:str, album:str, year:str, genre:str)->Track:
    """ Adds a track to the store, if this track doesn't exist yet. If the album/artist is not yet in the model it is added.
        Generates also a cover art file for the Track's Album if doesn't exist yet.
        Returns the Track.
    """
    album:Album = self.add_album( artist, album,year,genre) # Tracks's Album & Artist are now defined
    track:Track = Track( name, tracknumber, length, file)
    track = album.add_track( track)
    return track
  
  def add_track_from_dict( self, tags:dict)->Track:
    """ Adds a track to the store. The track dfinition is a dict object. If an attribute is missing, it is set to ''.
        Generates also a cover art file for the Track's Album if doesn't exist yet.
        Returns the track
    """
    file= tags.get('file','')
    name= tags.get('title','')
    tracknumber= tags.get('track','')
    length= tags.get('time','')
    artist= tags.get('artist','')
    album= tags.get('album','')
    year= tags.get('date','')
    genre= tags.get('genre','')
    res = self.add_track( file, name, tracknumber, length, artist, album, year, genre)
    if res.album is None:
      print( res.name +" has no album.")
    return res
  
  def get_artists(self, filter:str=None):
    if( filter is None):
      return [*self.keys()]
    else :
      return [ k for k in self.keys() if filter.casefold() in k.casefold() ]
    
