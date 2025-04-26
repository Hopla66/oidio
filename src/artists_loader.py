from datetime import datetime 
from mutagen.id3 import ID3
from io import BytesIO
from PIL import Image
import os

from config_loader import Config
from model import Track, Album, Artists
from mpd_admin import MPDAdmin

class ArtistsLoader():

  def __init__( self, config:Config):
    self.config = config

  def dump( self):
    """ dumps the artists list from mdp.
    """
    admin = MPDAdmin( self.config)
    admin.dump_db()

  def load( self, folders:list[str]=[], update_coverart:bool=False)->Artists:
    artists = Artists()
    do_filter = len( folders) > 0
    with open( self.config.get_music_db(), "r", encoding="utf-8") as file:
      l = file.readline()
      while l :
        tags = eval(l)
        if not do_filter or self.__match_folder( tags.get('file',''), folders) :
          self.__add_track_from_dict( artists, tags)
        l = file.readline()
    file.close()
    self.__set_cover_art( artists, update_coverart)
    return artists
  
  def __match_folder( self, file:str, folders:list[str])->bool:
    """ Checks if the file is in one of the folders.
        Returns True if the file is in one of the folders.
    """
    for folder in folders:
      if file.startswith( folder):
        return True
    return False

  def __set_cover_art( self, artists:Artists, update_coverart:bool=False):
    # loop thru albums to set coverart
    for artist in artists.values():
      for album in artist.albums:
        self.set_coverart( album, update_coverart)

  def __add_track_from_dict( self, artists:Artists, tags:dict)->Track:
    """ Adds a track to the store. The track definition is a dict object. If an attribute is missing, it is set to ''.
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
    res = artists.add_track( file, name, tracknumber, length, artist, album, year, genre)
    if res.album is None:
      print( res.name +" has no album.")
    return res
  
  def __exists_cover( self, album:Album):
    """ Checks if the cover file exists
        Returns the cover file name and if it exists
    """
    cover_name = album.id+".jpg"
    cover = os.path.join( self.config.get_coverart_cache(), cover_name)
    return cover_name, os.path.exists( cover)
      
  def __delete_cover( self, cover_name:str, album:Album):
    """ Deletes the cover file if it exists
    """
    try:
      os.remove( os.path.join( self.config.get_coverart_cache(), cover_name))
    except OSError as e:
      print( f"Error deleting file {cover_name} for album {album.name}: {e}")

  def set_coverart( self, album:Album, update_coverart:bool=False)->None:
    """ Sets the cover art for the album. If the cover file doesn't exist, it is created.
        If update_coverart is True, the cover file is always updated.
    """
    if len(album.tracks) == 0:
      return
    cover_name, exists_cover = self.__exists_cover( album)
    album.cover = cover_name if exists_cover else ""

    if update_coverart or not exists_cover:
      track = self.__find_track( album)
      if track is None:
        if exists_cover:
          self.__delete_cover( cover_name)
        return
      # regenerate cover file
      if not exists_cover or not self.__is_cover_uptodate( cover_name, track):
        img = ID3( track).getall("APIC")
        if( img is None or len(img) == 0 or img[0] is None):
          return
        album.cover = self.__dump_cover( img[0].data, cover_name)

  def __find_track( self, album:Album)->str|None:
    """ Finds a track file for the album. The track file is the first track in the album.
        Returns the track file name or None.
    """
    for track in album.tracks:
      res = self.config.get_track_path( track.file)
      if os.path.exists( res):
        return res
    return None
  

  def __is_cover_uptodate( self, cover_name:str, track_file:str)->bool:
    """Checks if the cover file is up to date: newer than the track file"""
    if track_file is None:
        return True
    cover_ts = datetime.fromtimestamp( os.path.getmtime( os.path.join( self.config.get_coverart_cache(), cover_name)))
    track_ts = datetime.fromtimestamp( os.path.getmtime(track_file))
    return cover_ts >= track_ts
  
  def __dump_cover( self, data, cover_name:str):
    """ Stores cover art image as file """
    cover = BytesIO( data)
    img = Image.open( cover)
    img = img.resize( [600, 600], Image.Resampling.NEAREST)
    img.save( os.path.join( self.config.get_coverart_cache(), cover_name), "JPEG")
    return cover_name