from fastapi import FastAPI, Response, WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel

import jsons
import json
import asyncio

from playerasync import Player
#from playerasync import Status
from model import Artist
from repository import REPOSITORY_FOLDER

import logging

# uvicorn main:app --reload

logger = logging.getLogger('uvicorn.error')

app = FastAPI()
app.mount( "/static", StaticFiles(directory=REPOSITORY_FOLDER), name="static")
app.mount( "/public", StaticFiles(directory="public",html = True), name="public")

mpd = Player(server="192.168.0.51", logger='uvicorn.error')
artists = mpd.loadDb('mpd.json')

mpd.connect()

socket = Player(server="192.168.0.51", logger='uvicorn.error')

@app.get("/")
def read_index():
    return FileResponse('public/index.html')

@app.get("/artists/")
def get_artists( filter:str|None=None):
    return {"artists" : artists.getArtists(filter) }

@app.get("/artist/{name}")
def get_artist( name:str):
    artist = artists.get( name)
    json = generateArtist( name)
    return Response(content=json, media_type='application/json')

def generateArtist( name:str)->str:
    artist = artists.get( name)
    return jsons.dumps( artist, strip_properties=True, strip_privates=True)

@app.get("/status")
async def get_status():
    s = await mpd.getStatus()
    return s


class PlayReq(BaseModel):
    song: str | None = None
    artist: str | None = None
    album: str | None = None

@app.post("/play/")
async def play( req:PlayReq):
    res = { "status" : "NOK"}
    if req.song is not None:
        try:
            res = await mpd.play( req.song)
        except Exception as ex:
            logger.info(f'#### error :: {ex}')
    else:
        logger.info( f'play {req.artist} {req.album}')
        try:
            album = artists.get( req.artist).getAlbum(req.album)
            tracks = []
            for track in album.tracks:
                await tracks.append( track.file)
            res = await mpd.playAlbum( tracks)
        except Exception as ex:
            logger.info(f'#### error :: {ex}')
    return res
    
@app.post("/control/play")
async def togglePlay():
    try:
        return await mpd.togglePlay()
    except Exception as ex:
        logger.info(f'#### error :: {ex}')
        return { "status" : "NOK"}
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info('#### websocket_endpoint')
    await websocket.accept()
    await socket.connect()
    logger.info('#### websocket_endpoint accepted')
    while True:
        data = await socket.idle()
        #data = await socket.getStatus()
        #await asyncio.sleep(5)
        logger.info(f'#### Websocket :: {data}')
        await websocket.send_text(json.dumps(data))
    





