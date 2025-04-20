from config_loader import Config
from artists_loader import ArtistsLoader
from model import Artists
import pytest
""""
def test_dump_mpd_db():
  config = Config()
  loader = ArtistsLoader( config)
  loader.dump_db()
"""
def test_load_mpd_db():
  config = Config()
  loader = ArtistsLoader( config)
  artists = loader.load_db()
  loader.dump_db( artists)
