from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from repository import dumpCover, existsCover

import uuid
import ffmpeg


class Tags(object):
  def __init__(self, path:str):
    self.track_info = MP3(path, ID3=EasyID3)
    self.path = path

  def getLength( self):
    length = float(ffmpeg.probe( self.path)['format']['duration'])
    return str(int(length/60)) + ':{:02}'.format(int(length%60))
  
  def getTag( self, tagName:str):
    if( tagName == 'length'):
      return self.getLength()
    try :
      return self.track_info[tagName][0]
    except:
      print("Tag not defined : "+ tagName)
      return ""

  def writeCoverImage( self, filename=None)->str:
    if filename == None:
      filename = uuid.uuid4().hex+".jpg"
    if existsCover(filename):
      return filename
    
    img = ID3(self.path).getall("APIC")
    if( img == None or len(img) == 0 or img[0] == None):
      return ""
    dumpCover( img[0].data, filename)
    return filename
  
  def __str__(self):
    return self.getTag('artist')+'::'+self.getTag('album')+'::'+self.getTag('tracknumber')+' - '+self.getTag('title')
  
"""

 print(EasyID3.valid_keys.keys())
 dict_keys(['album', 'bpm', 'compilation', 'composer', 'copyright', 'encodedby', 'lyricist', 'length', 'media', 'mood', 'grouping', 'title', 
 'version', 'artist', 'albumartist', 'conductor', 'arranger', 'discnumber', 'organization', 'tracknumber', 'author', 
 'albumartistsort', 'albumsort', 'composersort', 'artistsort', 'titlesort', 'isrc', 'discsubtitle', 'language', 'genre', 'date', 
 'originaldate', 'performer:*', 'musicbrainz_trackid', 'website', 'replaygain_*_gain', 'replaygain_*_peak', 
 'musicbrainz_artistid', 'musicbrainz_albumid', 'musicbrainz_albumartistid', 'musicbrainz_trmid', 'musicip_puid', 'musicip_fingerprint', 
 'musicbrainz_albumstatus', 'musicbrainz_albumtype', 'releasecountry', 'musicbrainz_discid', 'asin', 'performer', 'barcode', 'catalognumber', 
 'musicbrainz_releasetrackid', 'musicbrainz_releasegroupid', 'musicbrainz_workid', 'acoustid_fingerprint', 'acoustid_id'])

 """