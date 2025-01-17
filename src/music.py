from radios import RADIOS
import jsons

# uvicorn main:app --reload
"""
data =  {"song": {"file": "http://direct.fipradio.fr/live/fip-hifi.aac", "name": "fip-hifi.aac", "pos": "0", "id": "7"}, 
    "status": {"volume": "46", "repeat": "0", "random": "0", "single": "0", "consume": "0", "partition": "default", "playlist": "16", "playlistlength": "1", "mixrampdb": "0", "state": "play", "song": "0", "songid": "7", "time": "9212:0", "elapsed": "9212.340",
    "bitrate": "201", "audio": "48000:16:2"}
    }
    
data1 =   {"song": {"file": "http://icecast.radiofrance.fr/fipjazz-hifi.aac", "name": "fipjazz-hifi.aac", "pos": "0", "id": "3"}, 
           "status": {"volume": "46", "repeat": "0", "random": "0", "single": "0", "consume": "0", "partition": "default", "playlist": "8", 
                      "playlistlength": "1", "mixrampdb": "0", "state": "play", "song": "0", "songid": "3", "time": "134:0", "elapsed": "134.217", 
                      "bitrate": "232", "audio": "48000:16:2"}
}   
"""

class Music(object):
    """ Music element from mpd. """
    
    def __init__( self, mpdDef:dict):
        self.type = ""
        self.artist = ""
        self.album = ""
        self.title = ""
        self.length = 0
        self.elapsed = 0

        self.current = False

        self.__setType( mpdDef['song'])
        if( self.isRadio()):
            self.__initRadio( mpdDef['song'])
        elif ( self.isSong()):
            self.__initSong( mpdDef['song'])


        if( self.__isStatus(mpdDef)):
            self.__setPlayStatus( mpdDef['status'])
        else:
            self.current = ( self.file == mpdDef['current']['file'])
    

    def __setType( self, song:dict):
        if( bool(song) == False):
            return
        if 'album' in song:
            self.type = 'track'
        else:
            self.type = 'radio'

    def __setPlayStatus( self, status):
        if status['state'] != 'stop':
            time = status['time'].split(":") # <elapsed>:<length>
            self.length = time[1] 
            self.elapsed = time[0]        

    def __initSong( self, mpdDef):
        self.artist = mpdDef['artist']
        self.album = mpdDef['album']
        self.title = mpdDef['title']
        self.length = mpdDef['time']
        self.file = mpdDef['file']

    def __initRadio( self, mpdDef):
        self.artist = 'RADIOS'
        self.title = RADIOS.getName( mpdDef['file'])
        self.file = mpdDef['file']





    def isRadio( self):
        return self.type == 'radio'
    
    def isSong( self):
        return self.type == 'track'

        
    def __isStatus( self, item:dict):
        return ('status' in item)
    
"""
x = Music( data1)
json = jsons.dumps( x, strip_properties=True, strip_privates=True)
print( json)
"""