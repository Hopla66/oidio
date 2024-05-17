from  playerasync import Player

"""
p = Player("192.168.0.51")
print(p)
#p.play( "NAS/freebox/Codona/Codona/Codona - Codona - 01 - like that of sky.mp3")
#p.play( "NAS/freebox/Alain Bashung/Bleu Pétrole/Alain Bashung - Bleu Pétrole - 06 - Comme un lego.mp3")

print(p.client.currentsong())
print(p.client.status())
print(p.client.listplaylists())
print('########## default playlist')
print(p.client.listplaylist('Default Playlist'))
print('########## playlist info')
print(p.client.playlistinfo())

#p.client.pause()
status = p.client.status()
print(status)
#p.client.pause()
"""
"""
import asyncio

async def func_a(p:Player):
    print("Function A is running")
    status = p.client.status()
    print(status)
    print("Function A is done")
    return "Function A"

async def func_b(p:Player):
    print("Function B is running")
    while True:
        await waitEvent()
        status = p.client.status()
        print(status)
    return "Function B"

async def main( p:Player):
    print("Main function is running")
    results = await asyncio.gather(func_a(p), func_b(p))
    print("Main function is done")
    print(results)

async def waitEvent():
    p.client.idle('player')
    return "."

p = Player("192.168.0.51")
print(p)
asyncio.run(main( p))
"""
import asyncio
import json
import logging

async def main( p:Player):
    #await p.connect()
    while True:
        await p.idle()
        s = await p.getStatus()
        print( json.dumps(s))

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
p = Player("192.168.0.51", logger=__name__)
asyncio.run(main( p))