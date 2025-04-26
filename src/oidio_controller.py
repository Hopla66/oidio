import jsons

from playerasync import Player
from config_loader import Config
from model import Artists
from artists_loader import ArtistsLoader
from radios import Radios
from podcasts import Podcasts
from music import Music
 

class OidioController():

    def __init__( self, config:Config):
        self.mpd = Player( config)
        self.mpd_status = Player(config)
        self.artists_loader = ArtistsLoader( config)
        self.radios = Radios( config.get_radio_list())
        self.podcasts = Podcasts( config.get_radio_list(), config.get_rf_key())  

    def load_repo( self):
        self.artists = self.artists_loader.load()
        self.radios.load()
        #self.podcasts.load()  

    async def connect( self):
        await self.mpd.connect()
        await self.mpd_status.connect()

    def stop( self):
        self.mpd.stop()

    def get_artists(self, filter:str=None):
        artists = self.artists.get_artists(filter)
        return jsons.dumps( artists, strip_properties=True, strip_privates=True)

    def get_artist(self, name:str):
        artist = self.artists.get(name)
        return jsons.dumps( artist, strip_properties=True, strip_privates=True)

    def get_radios( self, filter:str=None):
        radios = self.radios.get_all()
        return jsons.dumps( radios, strip_properties=True, strip_privates=True)

    def get_podcasts( self, filter:str=None):
        podcasts = self.podcasts.get_list()
        return jsons.dumps( podcasts, strip_properties=True, strip_privates=True)

    async def get_status( self):
        mpd_status = await self.mpd.get_status()
        return self.__format_status( mpd_status)

    async def get_playlist( self):
        playlist_info = await self.mpd.get_playlist()
        res = []
        for song in playlist_info['list']:
            #self.log('getPlaylist '+json.dumps(song))

            m = Music( { 'song' : song, 'current' : playlist_info['current']}, self.radios)

            #elt = self.getPlaylistElt( song, current)
            res.append( m)
        return jsons.dumps( res, strip_properties=True, strip_privates=True)
    

    async def play( self, fname:str, volume:int=None, repeat:int=0):
        await self.mpd.play( fname, volume, repeat)
        return await self.get_status()
    
    async def toggle_play( self):
        await self.mpd.toggle_play()
        return await self.get_status()
    
    async def seek( self, secs):
        await self.mpd.seek( secs)
        return await self.get_status()
     
    async def play_next( self):
        await self.mpd.playNext()
        return await self.get_status()
 
    async def play_previous( self):
        await self.mpd.playPrevious()
        return await self.get_status()

    async def play_album( self, artist_name:str, album_name:str, volume:int=None, repeat:int=0):
        album = self.artists.get( artist_name).get_album(album_name)
        tracks = [ track.file for track in album.tracks]
        await self.mpd.playAlbum( tracks, volume, repeat)
        return await self.get_status()
    
    async def wait_for_event( self):
        await self.mpd_status.ping()
        status = await self.mpd_status.idle()
        return self.__format_status( status)
    
    def __format_status( self, mpd_status)->str:
        m = Music( mpd_status, self.radios)
        res = {
            "currentSong" : m,
            "state" : mpd_status['status']['state'],
            "volume" : mpd_status['status']['volume'],
            "repeat" : mpd_status['status']['repeat'],
            "random" : mpd_status['status']['random']
        }
        return  jsons.dumps( res, strip_properties=True, strip_privates=True)        
