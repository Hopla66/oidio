# We are going to test the configLoader.py file
from config_loader import Config

def test_config_default_file():
    config = Config()
    assert True

def test_config_provided_file():
    config = Config("/media/laurent/data/oidio/dvpt/oidio/cfg/config.json")
    assert True

def test_value_music_repository():
    config = Config()
    assert config.get_music_repository() == '/media/laurent/data/MUSIK/Music'

def test_value_coverart_cache():
    config = Config()
    assert config.get_coverart_cache() == '/media/laurent/data/oidio/cfg/cover_art_cache' 

def test_value_music_db():
    config = Config()
    assert config.get_music_db() == '/media/laurent/data/oidio/cfg/music_db.json'

def test_value_radio_list():
    config = Config()
    assert config.get_radio_list() == '/media/laurent/data/oidio/cfg/radios.json'

def test_value_rf_api():
    config = Config()
    assert config.get_rf_key() == '/media/laurent/data/oidio/cfg/rfApi.txt' 

def test_value_mpd_port():
    config = Config()
    assert config.get_MPD_port() == 6600
    

