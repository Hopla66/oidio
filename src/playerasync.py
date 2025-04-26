import asyncio

from mpd.asyncio import MPDClient

from config_loader import Config
from radios import Radios
from music import Music

from model import *
import os
import logging

import json

REPO = "/Users/Laurent/Python/data/mpd"


class Player(object):
    """ Interacts with mpd. """
    
    def __init__( self, config:Config, logger:str=''):
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.server = config.get_MPD_server()
        self.port = config.get_MPD_port()
        #await self.client.connect( server, port)      # connect to localhost:6600
        self.artists = Artists()
        if logger != '':
          self.logger = logging.getLogger( logger)
        else:
          self.logger = None
        self.radios = Radios( config.get_radio_list())

    def stop( self):
        #self.client.close()                     # send the close command
        self.client.disconnect() 

    def __str__( self):
        return self.client.mpd_version
    
    async def toggle_play( self):
        self.log( 'togglePlay ... ')
        await self.client.pause()
    
    def getType( self, song):
        if( bool( song) == False):
            return ''
        if 'album' in song:
            return 'track'
        else:
            return 'radio'

    
    async def get_status( self):
        self.log( 'getStatus ... ')
        await self.ping()
        current = await self.client.currentsong()
        status = await self.client.status()

        params = { 'song' :current, 'status' : status}
        self.log( "getStatus :: "+ json.dumps(params))
        return params

     
    async def get_playlist( self):
        self.log('getPlaylist ...')
        await self.ping()
        pl = await self.client.playlistinfo()
        current = await self.client.currentsong()
        return {'list' :pl, 'current' : current}
    
    def getPlaylistElt( self, song, current):
        if self.getType(song) == 'song':
            elt = { "artist" : song['artist'], "album" : song['album'], "title" : song['title'],
                    "length" :  song['time'],  "current" : bool(current) and (current['title'] == song['title'])
                  }
        else:
            elt = { "artist" : "Radio", "album" : "", "title" : self.radios.getName( song['file']),
                    "length" : 0, "current" : bool(current) and (current['file'] == song['file'])
                   }
        return elt

    async def idle( self):
        async for subsystem in self.client.idle(['player']):
            break
        return await self.get_status()


    async def ping( self):
        try:
            self.log("## ping ...")
            await self.client.ping()
        except Exception as inst:
            await self.connect()

    async def seek( self, secs):
        await self.client.seekcur( secs)
    
    async def playNext( self):
        await self.client.next()
 
    async def playPrevious( self):
        await self.client.previous()
 
    async def playAlbum( self, tracks:list[str], volume:int=None, repeat:int=0):
        await self.ping()
        self.setPlayParams( volume, repeat)
        await self.client.clear()
        for track in tracks:
            await self.client.add( track)
        await self.client.play()
    
    async def play( self, fname:str, volume:int=None, repeat:int=0):
        await self.ping()
        self.setPlayParams( volume, repeat)
        await self.client.clear()
        await self.client.add( fname)
        self.log( 'play : '+fname)
        await self.client.play()

    def setPlayParams( self, volume:int=None, repeat:int=1, single:int=0):
        if volume is not None:
          self.client.setvol( volume)
        self.client.repeat( repeat)
        self.client.single(single)

    async def connect(self):
        try:
            self.log("## connect ...")
            await self.client.connect( self.server, self.port)      
        except Exception as inst:
            self.log("## reconnect err")
            

    
    def log( self, msg:str):
        if self.logger is not None:
            self.logger.info( msg)
