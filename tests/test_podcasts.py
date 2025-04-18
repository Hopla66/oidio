from config_loader import Config
from podcasts import Podcasts
import pytest

def test_podcasts_no_files():
    with pytest.raises(FileNotFoundError) as excinfo:
      podcasts = Podcasts()
      podcasts.load()
    assert excinfo.type is FileNotFoundError

def test_podcasts_wrong_file():
    with pytest.raises(FileNotFoundError) as excinfo:
      podcasts = Podcasts( 'pipo')
      podcasts.load()
    assert excinfo.type is FileNotFoundError

def test_podcasts_with_config():
    config = Config()
    podcasts = Podcasts( config.get_radio_list(), config.get_rf_key())
    podcasts.load()
    assert podcasts is not None

