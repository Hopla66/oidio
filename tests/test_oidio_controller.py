import pytest
import json
import asyncio

from oidio_controller import OidioController
from config_loader import Config

def test_oidio_controller_init():
    # Assuming Config is a class that needs to be instantiated
    config = Config()
    
    controller = OidioController(config)
    
    assert controller is not None
    assert controller.mpd is not None
    assert controller.artists_loader is not None
    assert controller.radios is not None
    assert controller.podcasts is not None

def test_oidio_controller_load_repo():
    config = Config()
    controller = OidioController(config)
    
    # Assuming load_repo method populates the artists, radios, and podcasts
    controller.load_repo()
    
    assert controller.artists is not None
    assert controller.radios is not None
    assert controller.podcasts is not None

def test_radios_list():
    controller = OidioController( Config())
    controller.load_repo()
    s = controller.get_radios()
    radios = json.loads( s)
    assert len(radios) == 11

@pytest.mark.asyncio
async def  test_oidio_controller_status(): 
    controller = OidioController( Config())
    controller.load_repo()
    # Assuming connect method establishes a connection to the MPD server
    status = await controller.get_status()
    controller.stop()
    j = json.loads( status)
    assert j['state'] == 'play'
    assert j['currentSong']['file'] == 'http://direct.fipradio.fr/live/fip-hifi.aac' #'http://icecast.radiofrance.fr/fipjazz-hifi.aac'

def test_artists():
    controller = OidioController( Config())
    controller.load_repo()
    json = controller.get_artists()
    assert json == 'jljl'

def test_artist_Abba():
    controller = OidioController( Config())
    controller.load_repo()
    json = controller.get_artist( 'Abba')
    assert json is not None 




