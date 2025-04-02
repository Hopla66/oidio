from config_loader import Config
from playerasync import Player
import pytest

import mpd



@pytest.mark.asyncio
async def test_player_async():
    config = Config()
    player = Player(config)
    status = await player.getStatus()   
    assert status['state'] == 'play'
