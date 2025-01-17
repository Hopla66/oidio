import asyncio

from mpd.asyncio import MPDClient
from radios import RADIOS
from music import Music

from model import *
import os
import logging

import json

REPO = "/Users/Laurent/Python/data/mpd"


class Player(object):
    """ Interacts with mpd. """
    
    def __init__( self, server:str="localhost", port:str="6600", logger:str=''):
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.server = server
        self.port = port
        #await self.client.connect( server, port)      # connect to localhost:6600
        self.artists = Artists()
        if logger != '':
          self.logger = logging.getLogger( logger)
        else:
          self.logger = None

    def stop( self):
        self.client.close()                     # send the close command
        self.client.disconnect() 

    def __str__( self):
        return self.client.mpd_version
    
    async def togglePlay( self):
        self.log( 'togglePlay ... ')
        await self.client.pause()
    
    def getType( self, song):
        if( bool( song) == False):
            return ''
        if 'album' in song:
            return 'track'
        else:
            return 'radio'

    
    async def getStatus( self):
        self.log( 'getStatus ... ')
        await self.ping()
        current = await self.client.currentsong()
        status = await self.client.status()

        params = { 'song' :current, 'status' : status}
        self.log( "getStatus :: "+ json.dumps(params))

        m = Music( params)
        res = {
            "currentSong" : m,
            "state" : status['state'],
            "volume" : status['volume'],
            "repeat" : status['repeat'],
            "random" : status['random']
        }
        self.log( "## done ")
        #self.log( 'getStatus = '+json.dumps(res))
        return res
    
    async def getPlaylist( self):
        self.log('getPlaylist ...')
        pl = await self.client.playlistinfo()
        current = await self.client.currentsong()
        res = []
        for song in pl:
            self.log('getPlaylist '+json.dumps(song))

            m = Music( { 'current' :current, 'song' : song})

            #elt = self.getPlaylistElt( song, current)
            res.append( m)
        return res
    
    def getPlaylistElt( self, song, current):
        if self.getType(song) == 'song':
            elt = { "artist" : song['artist'], "album" : song['album'], "title" : song['title'],
                    "length" :  song['time'],  "current" : bool(current) and (current['title'] == song['title'])
                  }
        else:
            elt = { "artist" : "Radio", "album" : "", "title" : RADIOS.getName( song['file']),
                    "length" : 0, "current" : bool(current) and (current['file'] == song['file'])
                   }
        return elt

    async def idle( self):
        async for subsystem in self.client.idle(['player']):
            break
        return await self.getStatus()


    async def ping( self):
        try:
            self.log("## ping ...")
            await self.client.ping()
        except Exception as inst:
            await self.connect()

    async def playAlbum( self, tracks:list[str], volume:int=None, repeat:int=0):
        self.setPlayParams( volume, repeat)
        await self.client.clear()
        for track in tracks:
            await self.client.add( track)
        await self.client.play()
        return await self.getStatus()
       
    
    async def play( self, fname:str, volume:int=None, repeat:int=0):
        self.setPlayParams( volume, repeat)
        await self.client.clear()
        await self.client.add( fname)
        self.log( 'play : '+fname)
        await self.client.play()
        return await self.getStatus()

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
            
    def dumpDb( self, fname:str):
        self.ping()
        l = self.client.listallinfo()
        with open( os.path.join( REPO, "mpd2.json"), "w", encoding="utf-8") as file:
            for s in l:
                print(s)
                if s.get("file") != None:
                    file.write( str(s)+"\n")
        file.close()        

    def loadDb( self, fname:str)->Artists:
        with open( os.path.join( REPO, fname), "r", encoding="utf-8") as file:
            l = file.readline()
            while l :
                self.addTrackFromTags( l)
                l = file.readline()
        file.close()
        return self.artists

    def addTrackFromTags( self, l:str)->Track:
        tags = eval(l) 
        track = self.artists.addTrackFromDict( tags)
        return track
    
    def getRadios( self):
        return RADIOS.getList()
    
    def log( self, msg:str):
        if self.logger is not None:
            self.logger.info( msg)
