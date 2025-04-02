from radios import Radios

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
    
    def __init__( self, mpdDef:dict, radios:Radios):
        self.radios = radios
        self.type = ""
        self.artist = ""
        self.album = ""
        self.title = ""
        self.length = 0
        self.elapsed = 0

        self.current = False

        self.__set_type( mpdDef['song'])
        if( self.is_radio()):
            self.__init_radio( mpdDef['song'])
        elif ( self.is_song()):
            self.__init_song( mpdDef['song'])


        if( self.__is_status(mpdDef)):
            self.__set_play_status( mpdDef['status'])
        else:
            self.current = ( self.file == mpdDef['current']['file'])
    

    def __set_type( self, song:dict):
        if( bool(song) == False):
            return
        if 'album' in song:
            self.type = 'track'
        else:
            self.type = 'radio'

    def __set_play_status( self, status):
        if status['state'] != 'stop':
            time = status['time'].split(":") # <elapsed>:<length>
            self.length = time[1] 
            self.elapsed = time[0]        

    def __init_song( self, mpdDef):
        self.artist = mpdDef['artist']
        self.album = mpdDef['album']
        self.title = mpdDef['title']
        self.length = mpdDef['time']
        self.file = mpdDef['file']

    def __init_radio( self, mpdDef):
        self.artist = 'RADIOS'
        self.title = self.radios.get_name( mpdDef['file'])
        self.file = mpdDef['file']

    def is_radio( self):
        return self.type == 'radio'
    
    def is_song( self):
        return self.type == 'track'

        
    def __is_status( self, item:dict):
        return ('status' in item)
    
"""
x = Music( data1)
json = jsons.dumps( x, strip_properties=True, strip_privates=True)
print( json)
"""