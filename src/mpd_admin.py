import time
from mpd import MPDClient
from config_loader import Config

class MPDAdmin(object):
    def __init__( self, config:Config):
        self.config = config
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        #print( f"MPDAdmin created with server {config.get_MPD_server()}:{config.get_MPD_port()}")

    def connect( self):
        try:
            self.client.connect( self.config.get_MPD_server(), self.config.get_MPD_port())      
        except Exception as inst:
            print("## connect err")

    def dump_db( self):
        self.ping()
        l = self.client.listallinfo()
        with open(  self.config.get_music_db(), "w", encoding="utf-8") as file:
            for s in l:
                if s.get("file") != None:
                    file.write( str(s)+"\n")
        file.close()

    def stop( self):
        self.client.stop()
        print( "## MPDAdmin stop")

    def is_updating( self):
        self.ping()
        status = self.client.status()
        return status.get('updating_db') != None
    
    def update( self, folder:str):
        while self.is_updating():
            time.sleep( 1)
        self.ping()
        return self.client.update( folder)

    def ping( self):
        try:
            self.client.ping()
        except Exception as inst:
            self.connect()

