from config_loader import Config
from model import Artists
import pytest

def test_artists_no_file():
    with pytest.raises(FileNotFoundError) as excinfo:
      artists = Artists()
      artists.load()
    assert excinfo.type is FileNotFoundError

def test_artists_wrong_file():
    with pytest.raises(FileNotFoundError) as excinfo:
      artists = Artists('pipo')
      artists.load()
    assert excinfo.type is FileNotFoundError    

def test_artists_with_config():
    artists = Artists( Config().get_music_db())
    artists.load()
    assert artists is not None

def test_artists_list():
    artists = Artists( Config().get_music_db())
    artists.load()
    list = artists.get_artists()
    assert len(list) > 0

def test_artists_Codona():
    artists = Artists( Config().get_music_db())
    artists.load()
    list = artists.get_artists( 'Codona')
    assert len( list) == 1
    list = artists.get_artists( 'pipo')
    assert len( list) == 0
    
