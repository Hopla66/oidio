from fastapi import FastAPI, Response, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel

from config_loader import Config
from oidio_controller import OidioController

import logging

# uvicorn oidio_server:app --reload
# fastapi dev oidio_server.py --port 8010 --host 192.168.0.52


logger = logging.getLogger('uvicorn.error')
config = Config()
controller = OidioController(config)
controller.load_repo()

def response( body:str)->Response:
    return Response(content=body, media_type='application/json')

app = FastAPI()
app.mount( "/static", StaticFiles(directory=config.get_coverart_cache()), name="static")
app.mount( "/public", StaticFiles(directory="public",html = True), name="public")

@app.get("/")
async def read_index():
    await controller.connect()
    return FileResponse('public/index.html')

@app.get("/artists")
def get_artists( filter:str|None=None):
    json = '{"artists" : '+controller.get_artists( filter)+'}'
    return response(json)

@app.get("/artist/{name}")
def get_artist( name:str):
    json = controller.get_artist( name)
    return response(json)

@app.get("/radios/")
def get_radios( filter:str|None=None):
    radios = controller.get_radios()
    return response(radios)

@app.get("/status/playlist")
async def get_playlist():
    playlist = await controller.get_playlist()
    return response( playlist)

@app.get("/status")
async def get_status():
    status = await controller.get_status()
    return response(status)

class PlayReq(BaseModel):
    song: str | None = None
    artist: str | None = None
    album: str | None = None

@app.post("/play/")
async def play( req:PlayReq):
    try:
        if req.song is not None:
            res = await controller.play( req.song)
        else:
            res = await controller.play_album( req.artist, req.album)
        return response(res)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Error playing song: {ex}")


@app.post("/control/play")
async def togglePlay():
    try:
        res =  await controller.toggle_play()
        return response(res)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Error toggle: {ex}")

class SeekReq(BaseModel):
    secs: str

@app.post("/control/seek")
async def seek( req:SeekReq):
    try:
        res = await controller.seek( req.secs)
        return response(res)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Error seek ({req.secs}): {ex}")

@app.post("/control/next")
async def playNext():
    try:
        res= await controller.play_next()
        return response(res)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Error next: {ex}")
    
@app.post("/control/previous")
async def playPrevious():
    try:
        res = await controller.play_previous()
        return response(res)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Error previous: {ex}")

    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info('#### websocket_endpoint')
    await websocket.accept()
    logger.info('#### websocket_endpoint accepted')
    while True:
        data = await controller.wait_for_event()
        logger.info(f'#### Websocket :: {data}')
        await websocket.send_text(data)