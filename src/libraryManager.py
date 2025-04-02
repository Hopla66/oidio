from player import Player
from model import Artists
from config_loader import Config
from player import Player


import sys
import time
import os
from datetime import datetime
from mpd import MPDClient

class MPDAdmin(object):
    def __init__( self, config:Config):
        self.config = config
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        print( f"MPDAdmin created with server {config.get_MPD_server()}:{config.get_MPD_port()}")

    def connect( self):
        try:
            self.client.connect( self.config.get_MPD_server(), self.config.get_MPD_port())      
        except Exception as inst:
            print("## connect err")

    def dumpDb( self, fname:str):
        self.ping()
        l = self.client.listallinfo()
        with open( os.path.join( self.config.get_app_data(), fname), "w", encoding="utf-8") as file:
            for s in l:
                print(s)
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
            time.sleep( 2)
        self.ping()
        return self.client.update( folder)

    def ping( self):
        try:
            self.client.ping()
        except Exception as inst:
            self.connect()




class LibraryScanner(object):
    def __init__( self, config:Config):
        self.library = config.get_music_repository()
        self.mount_point = config.get_music_mount()
        self.last_scan_file = os.path.join( config.get_app_data(), "lastScan.txt")

    def __get_last_scan( self):
        try :
          last_scan = datetime.fromtimestamp( os.path.getmtime( self.last_scan_file))
        except:
          last_scan = datetime(1970,1,1)
        return last_scan
    
    def __set_last_scan( self):
        with open( self.last_scan_file, "w") as file:
            file.write( str(datetime.now()))
        file.close()
#NAS/MUSIK/Tord Gustavsen Trio/Opening/Tord Gustavsen Trio - Opening - 01 - The Circle.mp3'
#/media/laurent/data/MUSIK/Music/Tord Gustavsen Trio      
# .replace( self.library, self.mount_point)  
    def __has_changes( self, folder, scan_from):
        changed = [f.path for f in os.scandir(folder) if f.is_dir() and datetime.fromtimestamp( f.stat().st_mtime) > scan_from]
        return len( changed) > 0

    def scan( self, scan_from:datetime):
        if scan_from == None:
            scan_from = self.__get_last_scan()
        print( f"find all folders changed after {scan_from} in dir {self.library}: ")
        artists = [f.path for f in os.scandir(self.library) if f.is_dir() and (datetime.fromtimestamp( f.stat().st_mtime) > scan_from or self.__has_changes( f.path, scan_from))]
        print( f"artists : {artists}")
        """        
        folders = []
        for artist in artists:
            albums = [f.path for f in os.scandir(artist) if f.is_dir() and datetime.fromtimestamp( f.stat().st_mtime) > scan_from]
            if len( albums) == 0:
                folders.append( artist)
            else:
                folders.extend( albums)
        """
        folders = artists
        print( f" folders : {folders}")
        return folders
    
    def update_library( self, scan_from:datetime):
        folders = self.scan(scan_from)
        mpd = MPDAdmin( Config())
        mpd.connect()
        for folder in folders:
            repo_folder = folder.replace( self.library, self.mount_point)
            print( f"update {repo_folder}")
            mpd.update( repo_folder)
        mpd.stop()
        self.__set_last_scan()

    def dump_db( self, fname:str):
        mpd = MPDAdmin( Config())
        mpd.dumpDb( fname)


def get_arg_date( args):
    if len( args) == 0:
        return None
    else:
        return datetime.strptime( args[0], "%Y%m%d")

if __name__ == '__main__':
    args = sys.argv[1:]
    scan_arg = get_arg_date( args)
    scanner = LibraryScanner( Config())
    scanner.update_library( scan_arg)


#scanner.check_mpd()
"""
mpd = Player(server="192.168.0.51")
mpd.connect()
print ( f'mounts :  {mpd.client.listmounts()}')
print( f'status {mpd.client.status()}')
print( f'update {mpd.client.update("NAS/MUSIK/XTC/Skylarking")}')
print( f'list all {mpd.client.listall()}')

mpd.stop()

#print( mpd.getStatus())
#mpd.play('NAS/freebox/Kate Bush/The Red Shoes/Kate Bush - The Red Shoes - 09 - Constellation of the Heart.mp3')
#mpd.play('/mnt/NAS/freebox/Kate Bush/The Red Shoes/Kate Bush - The Red Shoes - 09 - Constellation of the Heart.mp3')

#print("update ...")
#mpd.updateMusicLibrary()

#print("dump ...")
#mpd.dumpDb( 'newList.json')

artists = loadDb( 'mpd.json')
print( f' nbArtists {artists.getArtists()}')

print( artists.getArtists( 'Roberto Fonseca'))

print( artists.getArtists( 'Various Artists'))

a =  artists.getArtists()
"""