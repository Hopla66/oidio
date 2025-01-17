from mpd import MPDClient
from model import *
import os
import logging


REPO = "/Users/Laurent/Python/data/mpd"

class Player(object):
    """ Interacts with mpd. """
    
    def __init__( self, server:str="localhost", port:str="6600", logger:str=''):
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.server = server
        self.port = port
        #self.client.connect( server, port)      # connect to localhost:6600
        self.artists = Artists()
        if logger != '':
          self.logger = logging.getLogger( logger)
        else:
          self.logger = None

    def stop( self):
        self.client.close()                     # send the close command
        self.client.disconnect() 

    def __str__( self):
        return self.client.mpd_version
    
    def togglePlay( self):
        self.ping()
        self.client.pause()
        return self.getStatus()

    def getStatus( self):
        self.ping()
        song = self.client.currentsong()
        status = self.client.status()
        if status['state'] != 'stop':
            song['duration'] = status['time']
            song['elapsed'] = status['elapsed']
        res = {
            "type" : self.getType( song),
            "currentSong" : song,
            "state" : status['state'],
            "volume" : status['volume'],
            "repeat" : status['repeat'],
            "random" : status['random']
        }
        return res
    
    def getType( self, song):
        if 'album' in song:
            return 'track'
        else:
            return 'radio'

    def find( self, searchString:str, type:str='any'):
        self.ping()
        return self.client.find( type, searchString)
    
    def playAlbum( self, tracks:list[str], volume:int=None, repeat:int=0):
        self.ping()
        self.setPlayParams( volume, repeat)
        self.client.clear()
        for track in tracks:
            self.client.add( track)
        self.client.play()
        return self.getStatus()
       
    
    def play( self, fname:str, volume:int=None, repeat:int=0):
        self.ping()
        self.setPlayParams( volume, repeat)
        self.client.clear()
        self.client.add( fname)
        self.log( 'play : '+fname)
        self.client.play()
        return self.getStatus()

    def setPlayParams( self, volume:int=None, repeat:int=1, single:int=0):
        if volume is not None:
          self.client.setvol( volume)
        self.client.repeat( repeat)
        self.client.single(single)

    def idle( self):
        self.ping()
        self.client.idle('player')

    def ping( self):
        try:
            self.client.ping()
        except Exception as inst:
            self.connect()

    def connect(self):
        try:
            self.client.connect( self.server, self.port)      
        except Exception as inst:
            self.log("## reconnect err")

    def dumpDb( self, fname:str):
        self.ping()
        l = self.client.listallinfo()
        with open( os.path.join( REPO, "mpd2.json"), "w", encoding="utf-8") as file:
            for s in l:
                print(s)
                if s.get("file") != None:
                    file.write( str(s)+"\n")
        file.close()        

    def loadDb( self, fname:str)->Artists:
        with open( os.path.join( REPO, fname), "r", encoding="utf-8") as file:
            l = file.readline()
            while l :
                self.addTrackFromTags( l)
                l = file.readline()
        file.close()
        return self.artists

    def addTrackFromTags( self, l:str)->Track:
        tags = eval(l) 
        track = self.artists.addTrackFromDict( tags)
        return track
    
    def log( self, msg:str):
        if self.logger is not None:
            self.logger.info( msg)

"""   
p = Player("192.168.0.51")
print(p)

l = p.loadDb('mpd.json')
print( len(l))
x = l.getArtists()
print( x)
p.stop()
"""


#s = p.find( "like that of sky")
#s = p.find( "Codona2")

#s = p.client.playlist() #current playlist
#s = p.client.listplaylists()
#s = p.client.status()
#print(s)
#p.client.clear()
#s = p.client.playlist()
#l = p.client.listallinfo()

#song = "Codona2/Codona 2/Codona - Codona 2 - 02 - Godumaduma.mp3"
#l = p.client.sticker_set('song', song, 'cover', 'pipo.jpg')
#print(l)
#p1 = p.client.albumart(song)
#p2 = p.client.readpicture(song)

#print( p2.binary)
#l = p.client.sticker_set('song', song, 'cover', 'pipo.jpg')
#print(l)
#l = p.client.sticker_get('song', song, 'cover')
#print(l)
"""
with open( os.path.join( "/Users/Laurent/Python/data/mpd", "mpd2.json"), "w", encoding="utf-8") as file:
    for s in l:
        print(s)
        if s.get("file") != None:
            file.write( str(s)+"\n")
    file.close()
"""

#p.play( "NAS/freebox/Codona/Codona/Codona - Codona - 01 - like that of sky.mp3")
#p.client.volume(+20)
#print( p.client.commands())
#p.stop()