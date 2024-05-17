from datetime import datetime
from io import BytesIO
from PIL import Image

import os

REPOSITORY_FOLDER = "/Users/Laurent/Python/data/repository"
MUSIC_FOLDERS = { 'NAS/freebox' : 'Z:'}

def getCoverArtImage( fname:str)->str:
    """ Builds the full pathname of a cover art file """
    return os.path.join( REPOSITORY_FOLDER, fname)

def getTrackFile( fname:str)->str:
    """ Builds the full pathname of a track file. """
    return os.path.join( 'Z:', fname.replace('NAS/freebox',''))

def dumpCover( data, fname:str):
    """ Stores cover art image as file """
    cover = BytesIO( data)
    img = Image.open( cover)
    img = img.resize( [600, 600], Image.Resampling.NEAREST)
    img.save( os.path.join( REPOSITORY_FOLDER, fname))

def existsCover(fname:str)->bool:
    """ Checks if the cover file already exists """
    f = os.path.join( REPOSITORY_FOLDER, fname)
    return os.path.exists(f)

def isCoverUptodate( coverName:str, fileName:str)->bool:
    """Checks if the cover file is uptodate"""
    if fileName is None:
        return True
    coverTs = datetime.fromtimestamp( os.path.getmtime( os.path.join( REPOSITORY_FOLDER, coverName)))
    fTs = datetime.fromtimestamp( os.path.getmtime( getTrackFile( fileName)))
    return coverTs >= fTs



"""
def dump(obj):
    if isinstance( obj, Album):
        json = generateAlbum( obj)
        fname = obj.id+".json"
    elif isinstance( obj, Artist):
        print("### dump "+obj.name+" has "+str(len(obj.albums))+" albums")
        json = generateArtist( obj)
        fname = obj.id+".json"
    elif isinstance( obj, dict):
        json = generateArtistList( obj)
        fname = "artists.json"
            
    with open( os.path.join( REPOSITORY_FOLDER, fname), "w") as file:
        file.write( json)
        file.close()

def generateArtistList(list:dict)->str:
    return jsons.dumps( list.values(), strip_attr='albums',strip_properties=True, strip_privates=True, jdkwargs={"indent":2})

def generateArtist(artist:Artist)->str:
    return jsons.dumps( artist, strip_properties=True, strip_privates=True, jdkwargs={"indent":2})

def generateAlbum(album:Album)->str:
    return jsons.dumps( album, strip_properties=True, strip_privates=True, jdkwargs={"indent":2})
"""

""" 
def loadArtist( fname:str)->Artist:
    with open( os.path.join( REPOSITORY_FOLDER, fname), 'r') as file:
        data = file.read()
    a = jsons.loads( data, Artist)
    a.check()
    return a

def loadArtists( fname:str)->dict[str,Artist]:
    with open( os.path.join( REPOSITORY_FOLDER, fname), 'r') as file:
        data = file.read()
      
    l = jsons.loads( data, list[Artist])
    res =  Artists()
    for a in l:
        print("load "+a.name+"  "+a.id)
        artist = loadArtist( a.id+".json")
        res.add( artist)
    return res
"""
"""
artists = loadArtists( 'artists.json')
for a in artists.values():
    a.list()
print(len(artists))
"""    
