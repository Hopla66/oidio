from config_loader import Config
from artists_loader import ArtistsLoader
from model import Artists
import pytest
""""
def test_dump_mpd_db():
  config = Config()
  loader = ArtistsLoader( config)
  loader.dump_db()

def test_load_mpd_db():
  config = Config()
  loader = ArtistsLoader( config)
  artists = loader.load()
  loader.dump( artists)
"""

def test_artists_list():
  artists = ArtistsLoader( Config()).load()
  list = artists.get_artists()
  assert len(list) > 0

def test_artists_Codona():
  artists = ArtistsLoader( Config()).load()
  list = artists.get_artists( 'Codona')
  assert len( list) == 1
  assert len( artists.get('Codona').albums) == 3
  list = artists.get_artists( 'pipo')
  assert len( list) == 0  

def test_artists_Abba():
  artists = ArtistsLoader( Config()).load()
  list = artists.get_artists( 'Abba')
  assert len( list) == 1
  assert len( artists.get('Abba').albums) == 1
