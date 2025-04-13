# We are going to test the configLoader.py file
from config_loader import Config
import os

LOCAL_OIDIO_DATA = "/Users/Laurent/Python/data/cfg"
RPI_OIDIO_DATA = "/media/laurent/data/oidio/cfg"

LOCAL_MUSIC_REPOSITORY ="/Users/Laurent/Python/data/Musik"
RPI_MUSIC_REPOSITORY ="/media/laurent/data/MUSIK/Music"

OIDIO_DATA = LOCAL_OIDIO_DATA
MUSIC_REPOSITORY = LOCAL_MUSIC_REPOSITORY

def test_config_default_file():
    config = Config()
    assert True

def test_config_provided_file():
    config = Config( "../cfg/config.json")
    assert True

def test_value_music_repository():
    config = Config()
    assert config.get_music_repository() == MUSIC_REPOSITORY

def test_value_coverart_cache():
    config = Config()
    assert config.get_coverart_cache() == os.path.normpath(OIDIO_DATA+ '/cover_art_cache' )

def test_value_music_db():
    config = Config()
    assert config.get_music_db() == os.path.normpath(OIDIO_DATA+ '/music_db.json')

def test_value_radio_list():
    config = Config()
    assert config.get_radio_list() == os.path.normpath(OIDIO_DATA+ '/radios.json')

def test_value_rf_api():
    config = Config()
    assert config.get_rf_key() == os.path.normpath(OIDIO_DATA+ '/rfApi.txt' )

def test_value_mpd_port():
    config = Config()
    assert config.get_MPD_port() == 6600

def test_file_path():
    config = Config()
    assert config.get_file_path("NAS/MUSIK/Tord Gustavsen Trio/Opening/Tord Gustavsen Trio - Opening - 01 - The Circle.mp3")  == os.path.normpath( MUSIC_REPOSITORY + "/Tord Gustavsen Trio/Opening/Tord Gustavsen Trio - Opening - 01 - The Circle.mp3")
    

