import jsons

from playerasync import Player
from config_loader import Config
from model import Artists
from radios import Radios
from podcasts import Podcasts
 

class OidioController():

    def __init__( self, config:Config):
        self.mpd = Player( config)
        self.artists = Artists( config.get_app_data())
        self.radios = Radios( config.get_app_data())
        self.podcasts = Podcasts( config.get_app_data())  

    def load_repo( self):
        self.artists.load()
        self.radios.load()
        self.podcasts.load()  

    def connect( self):
        self.mpd.connect()

    def get_artists(self, filter:str):
        return self.artists.get_artists(filter)

    def get_artist(self, name:str):
        artist = self.artists.get(name)
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