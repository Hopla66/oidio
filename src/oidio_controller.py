import jsons

from playerasync import Player
from config_loader import Config
from model import Artists
from radios import Radios
from podcasts import Podcasts
 

class OidioController():

    def __init__( self, config:Config):
        self.mpd = Player( config)
        self.artists = Artists( config.get_music_db())
        self.radios = Radios( config.get_radio_list())
        self.podcasts = Podcasts( config.get_radio_list(), config.get_rf_key())  

    def load_repo( self):
        self.artists.load()
        self.radios.load()
        self.podcasts.load()  

    def connect( self):
        self.mpd.connect()

    def get_artists(self, filter:str|None):
        return self.artists.get_artists(filter)

    def get_artist(self, name:str):
        artist = self.artists.get_artists(name)
        return jsons.dumps( artist, strip_properties=True, strip_privates=True)

    def get_radios( self, filter:str):
        radios = self.radios
        return jsons.dumps( radios, strip_properties=True, strip_privates=True)

    def get_podcasts( self, filter:str):
        podcasts = self.podcasts
        return jsons.dumps( podcasts, strip_properties=True, strip_privates=True)

    async def get_status( self):
        status = await self.mpd.get_status()
        return  jsons.dumps( status, strip_properties=True, strip_privates=True)

    async def get_playlist( self):
        playlist = await self.mpd.get_playlist()
        return playlist
    
    async def play( self, fname:str, volume:int=None, repeat:int=0):
        res = await self.mpd.play( fname, volume, repeat)
        return res
    
    async def seek( self, secs):
        res = await self.mpd.seek( secs)
        return res
     
    async def play_next( self):
        res = await self.mpd.playNext()
        return res
 
    async def play_previous( self):
        res = await self.mpd.playPrevious()
        return res       

    async def play_album( self, tracks:list[str], volume:int=None, repeat:int=0):
        res = await self.mpd.playAlbum( tracks, volume, repeat)
        return res

