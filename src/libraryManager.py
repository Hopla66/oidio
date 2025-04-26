from config_loader import Config
from mpd_admin import MPDAdmin
from artists_loader import ArtistsLoader

import sys

import os, time
from datetime import datetime

class LibraryScanner(object):
    def __init__( self, config:Config):
        self.library = config.get_music_repository()
        self.last_scan_file = os.path.join( config.get_app_data(), "lastScan.txt")
        self.config= config

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
    def __has_changes( self, folder, scan_from):
        changed = [f.path for f in os.scandir(folder) if f.is_dir() and datetime.fromtimestamp( f.stat().st_mtime) > scan_from]
        return len( changed) > 0

    def scan( self, scan_from:datetime):
        if scan_from == None:
            scan_from = self.__get_last_scan()
        print( f"find all folders changed after {scan_from} in dir {self.library}: ")
        folders = [f.path for f in os.scandir(self.library) if f.is_dir() and (datetime.fromtimestamp( f.stat().st_mtime) > scan_from or self.__has_changes( f.path, scan_from))]
        print( f"## scanned folders : {folders}")
        return folders
    
    def update_library( self, scan_from:datetime):
        scan = self.scan(scan_from)
        folders = list( map( lambda f : os.path.join( self.config.get_music_mount(),  os.path.basename(f)), scan))
        mpd = MPDAdmin( self.config)
        mpd.connect()
        for folder in folders:
            print( f"update {folder}")
            mpd.update( folder)
        mpd.stop()
        self.__set_last_scan()
        return folders

    def dump_db( self):
        time.sleep(3)
        MPDAdmin( self.config).dump_db()



def get_arg_date( args):
    if len( args) == 0:
        return None
    else:
        return datetime.strptime( args[0], "%Y%m%d")

if __name__ == '__main__':
    args = sys.argv[1:]
    scan_arg = get_arg_date( args)
    config = Config()
    scanner = LibraryScanner( config)
    folders = scanner.update_library( scan_arg)
    scanner.dump_db()
    if len( folders) == 0:
        print( "No folder changed since last scan.")
        sys.exit(0)
    loader = ArtistsLoader( config)
    loader.load( folders, True)

