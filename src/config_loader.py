import json
import os

CONFIG_FOLDER = "../cfg/"


#    "music_repository": "/media/laurent/data/MUSIK/Music",
#    "music_mount": "NAS/MUSIK/",


class Config():
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.__load_config()

    def __load_config(self):
        with open( self.__get_full_path(self.config_file), 'r') as f:
            return json.load(f)

    def get_file_path( self, file:str)->str:
        """ Return the real path of a file in the musik folder"""
        return os.path.normpath(os.path.join( self.get_music_repository(), file.replace( self.get_music_mount(),'')))
    
    def get_app_data(self):
        return self.config.get('oidio_data')
    
    def __get_in_app_data(self, key):
        value = self.config.get(key)
        return os.path.normpath(self.__get_full_path( value, self.get_app_data()))
    
    def get_music_repository(self):
        return self.config.get('music_repository')
    
    def get_music_mount(self):
        return self.config.get('music_mount')
    
    def get_coverart_cache(self):
        return self.__get_in_app_data('cover_art_cache')
    
    def get_music_db(self):
        return self.__get_in_app_data('music_db')
    
    def get_MPD_server(self):
        return self.config.get('mpd_server')
    
    def get_MPD_port(self):
        res = self.config.get('mpd_port')
        if res == None:
            return 6600
        return res
    
    def get_radio_list(self):
        return self.__get_in_app_data('radio_list')
    
    def get_rf_key(self):
        return self.__get_in_app_data('rf_key')
    
    def __get_full_path(self, path, parent=CONFIG_FOLDER):
        if parent == None or path == None or path[0] == '/' or path[0] == '.':
            return path
        return os.path.normpath( os.path.join( parent, path))