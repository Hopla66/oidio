import hashlib
from mutagen.id3 import ID3
from repository import dumpCover, existsCover, getTrackFile, isCoverUptodate

import os

def createId( artist:str, album:str='')->str:
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
  def __init__( self, name, tracknumber, length, file, album:Album=None):
    self.name = name
    self.tracknumber = tracknumber
    self.length = length
    self._album = album
    self.file = file

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
    self.name = name
    self.year = year
    self.genre = genre
    self._artist = artist
    self.cover = ""
    self.folder = ""
    if tracks is None or len(tracks) == 0:
      self.tracks = []
    else:
      self.tracks = tracks
      self.folder = os.path.dirname( tracks[0].file)
    self.id = createId( name)

  def addTrack( self, track:Track)->Track:
    """ Adds a Track to this Album, if the Track doesn't exist yet"""
    t = self.getTrack( track.name)
    if t is None:
      self.tracks.append(track)
      track.album = self
      self.folder =os.path.dirname( track.file)
      self.writeCoverArt()
      return track
    else:
      return t

  def getTrack( self, trackName:str)->Track:
    for t in self.tracks:
      if( t.name == trackName):
        return t
    return None
  
  def check( self):
    for t in self.tracks:
      t.album = self

  def updateCoverArt( self):
    if self.cover == "":
      self.writeCoverArt()
    if isCoverUptodate( self.cover, self.tracks[0].file) == False:
      self.writeCoverArt()

  def writeCoverArt( self, force:bool=False):
      """ Creates a cover art file for this album if the cover art is not yet defined.
          Extracts the cover art from the first Track of this Album; assuming all tracks have cover art embedded in tag APIC.
          Assumes Album's Artist is defined, because both their names are used to create the file name.
      """
      if self.cover != "" and not force:
        return
      filename = self.id+".jpg"
      if not existsCover(filename) or force:
        path = getTrackFile(self.tracks[0].file)
        if( os.path.exists(path) == False):
           return
        img = ID3( path).getall("APIC")
        if( img is None or len(img) == 0 or img[0] is None):
          return ""
        dumpCover( img[0].data, filename)
      self.cover = filename

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
    self.id = createId( value.name, self.name)


  def __str__(self):
    return "<Album "+self.name+">"

#
#
class Artist(object):
  def __init__( self, name:str, id:str='', albums:list[Album]=None):
    if albums is None:
      self.albums = []
    else:
      self.albums = albums
    self.name = name
    self.id = createId( name)

  def addAlbum( self, album:Album)->Album:
    a = self.getAlbum(album.name)
    if a is None:
      a = album
      self.albums.append( a)
      a.artist = self
    return a
  
  def getAlbum( self, albumName:str)->Album:
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

  def addArtist( self, name:str):
    """ Creates a new Artist and adds it to the store if it doesn't exist yet. Returns the Artist."""
    item:Artist = self.get(name) 
    if( item is None):
      a = Artist( name)
      self.add( a)
      return a
    else:
      return item

  def addAlbum( self, artist, albumName, year, genre)->Album:
    """ Adds an Album to the store, if this Album doesn't exist yet. If the Album's Artist doesn't exist yet in the model, it is added. 
        Returns the Album.
    """
    a = self.addArtist( artist)
    album = Album( albumName, year, genre)
    album = a.addAlbum( album)
    return album
  
  def addTrack( self, file:str, name:str, tracknumber:str, length:str, artist:str, album:str, year:str, genre:str)->Track:
    """ Adds a track to the store, if this track doesn't exist yet. If the album/artist is not yet in the model it is added.
        Generates also a cover art file for the Track's Album if doesn't exist yet.
        Returns the Track.
    """
    album = self.addAlbum( artist, album,year,genre) # Tracks's Album & Artist are now defined
    track = Track( name, tracknumber, length, file)
    track = album.addTrack( track)
    return track
  
  def addTrackFromDict( self, tags:dict)->Track:
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
    res = self.addTrack( file, name, tracknumber, length, artist, album, year, genre)
    if res.album is None:
      print( res.name +" has no album.")
    return res
  
  def getArtists(self, filter:str=None):
    if( filter is None):
      return [*self.keys()]
    else :
      return [ k for k in self.keys() if filter.casefold() in k.casefold() ]
    
  def updateCoverArt( self, artistName:str=None):
    if artistName is not None:
      artist:Artist = self.get(artistName)
      if artist is not None:
        self.updateArtistCoverArt( artist)
    else: 
      for artist in self.values():
        self.updateArtistCoverArt( artist)

  def updateArtistCoverArt( self, artist:Artist):
      for album in artist.albums:
        tName:str = getTrackFile( album.tracks[0].file)
        if not isCoverUptodate( album.cover, tName):
          album.writeCoverArt( True)


