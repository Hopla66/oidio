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
from config_loader import Config

import logging

# uvicorn main:app --reload

logger = logging.getLogger('uvicorn.error')
config = Config()

app = FastAPI()
app.mount( "/static", StaticFiles(directory=config.get_music_repository()), name="static")
app.mount( "/public", StaticFiles(directory="public",html = True), name="public")

mpd = Player( config.get_MPD_server(), logger='uvicorn.error')
artists = mpd.loadDb('mpd.json')

#mpd.connect()

socket = Player( config.get_MPD_server(), logger='uvicorn.error')

@app.get("/")
async def read_index():
    await mpd.connect()
    return FileResponse('public/index.html')



@app.get("/artists/")
def get_artists( filter:str|None=None):
    return {"artists" : artists.get_artists(filter) }

@app.get("/artist/{name}")
def get_artist( name:str):
    artist = artists.get( name)
    json = jsons.dumps( artist, strip_properties=True, strip_privates=True)
    return Response(content=json, media_type='application/json')

@app.get("/radios/")
def get_radios( filter:str|None=None):
    radios = mpd.getRadios()
    json = jsons.dumps( radios, strip_properties=True, strip_privates=True)
    return Response(content=json, media_type='application/json')

@app.get("/status")
async def get_status():
    s = await mpd.getStatus()
    json = jsons.dumps( s, strip_properties=True, strip_privates=True)
    return Response(content=json, media_type='application/json')

@app.get("/status/playlist")
async def get_playlist():
    p = await mpd.getPlaylist()
    return p

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
                tracks.append( track.file)
            res = await mpd.playAlbum( tracks)
        except Exception as ex:
            logger.info(f'#### error :: {ex}')
    return res

class SeekReq(BaseModel):
    secs: str

@app.post("/control/seek")
async def seek( req:SeekReq):
    res = { "status" : "NOK"}
    logger.info( f'seek current song to {req.secs}s ...')
    try:
        res = await mpd.seek( req.secs)
    except Exception as ex:
            logger.info(f'#### error :: {ex}')
    return res

@app.post("/control/next")
async def playNext():
    try:
        return await mpd.playNext()
    except Exception as ex:
        logger.info(f'#### error :: {ex}')
        return { "status" : "NOK"}
    
@app.post("/control/previous")
async def playPrevious():
    try:
        return await mpd.playPrevious()
    except Exception as ex:
        logger.info(f'#### error :: {ex}')
        return { "status" : "NOK"}

@app.post("/control/play")
async def togglePlay():
    try:
        return await mpd.toggle_play()
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
        json = jsons.dumps( data, strip_properties=True, strip_privates=True)
        logger.info(f'#### Websocket :: {json}')
        await websocket.send_text(json)
    





