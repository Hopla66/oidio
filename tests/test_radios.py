from config_loader import Config
from radios import Radios
import pytest

def test_radios_no_file():
    with pytest.raises(FileNotFoundError) as excinfo:
      radios = Radios()
      radios.load()
    assert excinfo.type is FileNotFoundError

def test_radios_wrong_file():
    with pytest.raises(FileNotFoundError) as excinfo:
      radios = Radios( 'pipo')
      radios.load()
    assert excinfo.type is FileNotFoundError

def test_radios_with_config():
    radios = Radios( Config().get_radio_list())
    assert radios is not None

def test_get_cover():
   radios = Radios( Config().get_radio_list())
   radios.load()
   assert radios.get_cover( 'http://direct.fipradio.fr/live/fip-hifi.aac') == 'FIP.jpg'

def test_radios_list():
    radios = Radios( Config().get_radio_list())
    radios.load()
    assert len(radios.get_list()) == 11