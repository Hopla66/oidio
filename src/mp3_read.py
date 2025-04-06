
import os

from model import *
from tags import *
from repository import *

#MUSIC_REPO = "/mnt/NAS/freebox"
#MUSIC_REPO = "Z:"
MUSIC_REPO = "G:\MUSIK\Music"


# 
#
def addTrackFromTags( repo:Artists, song)->Track:
    tags = Tags( song)
    track = repo.add_track( song, tags.getTag('title'), tags.getTag('tracknumber'), tags.getTag('length'),
                           tags.getTag('artist'), tags.getTag('album'), tags.getTag('date'), tags.getTag('genre'))
    if track.album == None:
      print( track.name +" has no album ::"+tags.getTag('album')+" :: "+track.album.name)
    elif track.album.cover == "":
      track.album.cover = tags.writeCoverImage( track.album.id+".jpg")
    return track

 
##
##
ARTISTS = Artists()

def parseArtistFolder( fname):
  folder = os.path.join( MUSIC_REPO, fname)
  for root, dirs, files in os.walk(folder):
    for name in files:
      if name.endswith((".mp3")):
        print( "  parse Track :"+name) 
        song  = os.path.join( root, name)
        addTrackFromTags( ARTISTS, song)
        
def parseMusicRepository( repo):
  for artist in  next(os.walk( repo))[1]: 
      print("parse Artist : "+artist)
      parseArtistFolder( artist)

#parseMusicRepository( MUSIC_REPO)
#parseArtistFolder( os.path.join( MUSIC_REPO, "Gloria Gaynor"))
#parseArtistFolder( os.path.join( MUSIC_REPO, "William Sheller"))
#parseArtistFolder( os.path.join( MUSIC_REPO, "Charles Lloyd"))

"""
print('Dump all')
dump( ARTISTS)
for artist in ARTISTS.values():
  dump( artist)
"""
