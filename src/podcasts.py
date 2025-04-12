from model import *

import json
import datetime
import requests
import os


class Podcasts(Artists):
  """ A Podcast episode is a track of a fake Album named 'title of the podcast' of a fake Artist named 'Podcast' """
    
  URL = "https://openapi.radiofrance.fr/v1/graphql"
  KEY = ""
  
  def __init__( self, file:str='radios.json', rfKey:str='rfApi.txt'):
    self.config_file = file
    Podcasts.__get_rfapi_Key( rfKey)

  
  def load( self):  #load and cache the podcasts
    with open( self.config_file, encoding='utf-8') as json_data:
      list = filter( lambda x : x['type'] == 'podcast',json.load(json_data))
      for r in list:
        self.load_podcast( r)
    
  @staticmethod
  def __get_rfapi_Key( filename:str):
    if Podcasts.KEY == "":
      with open( filename) as key_file:
        Podcasts.KEY = key_file.read()
              
  @staticmethod
  def __build_query_rf( podcastUrl:str):
    return '{ "query" : "{ diffusionsOfShowByUrl( url: \\"'+ podcastUrl+'\\" first: 20) { edges { node { id published_date podcastEpisode { url title } }}}}"}'
  
  def load_podcast( self, metadata):
    query = Podcasts.__build_query_rf( metadata['file'])
    r = requests.post( Podcasts.URL, headers={"x-token": Podcasts.KEY, 'Content-Type': 'application/json'}, data=query)
    data = json.loads(r.text)
    for i, podcast in enumerate( data['data']['diffusionsOfShowByUrl']['edges'], 1):
      if podcast['node']['podcastEpisode'] is not None:
        title = podcast['node']['podcastEpisode']['title']
        url = podcast['node']['podcastEpisode']['url']
        podcastDate = datetime.datetime.fromtimestamp( int(podcast['node']['published_date'])).strftime('%Y-%m-%d')
        t = self.add_track( url, title, i, 0, 'Podcast', metadata['name'], '', '')
        t.cover = metadata['cover']
        t.album.cover = t.cover
        
  def get_podcast( self, name:str)->Album:
    """ Retrives the episodes of a given Podcast """
    return self.get_list().get_album( name)
        
  def get_list( self)->Artist:
    """ Returns the list of all the Podcasts """    
    return self.get('Podcast')
    
# def addTrack( self, file:str, name:str, tracknumber:str, length:str, artist:str, album:str, year:str, genre:str)->Track:
#SONG_QUERY =  "{ live(station: FIP_JAZZ) { song { id start end track { id  mainArtists title albumTitle productionDate } } }}"
#JAZZ_FIP_QUERY1=  '{ showByUrl( url: \\"https://www.radiofrance.fr/fip/podcasts/club-jazzafip\\") { id title diffusionsConnection { edges { node { title id published_date podcastEpisode { url } } } } } }'
#JAZZ_FIP_QUERY2='{show(id : \\"13d4ef2f-2aca-4331-949b-bc8da638d670_7\\"){id title diffusionsConnection {edges {node {title podcastEpisode {url}}}} }}'
#  JAZZ_FIP_QUERY3='{ diffusionsOfShowByUrl( url: \\"https://www.radiofrance.fr/fip/podcasts/club-jazzafip\\" first: 20) { edges { node { id published_date podcastEpisode { url title } }}}}'

#PODCASTS = Podcasts()

#if __name__ == "__main__":
#   jaF = PODCASTS.getPodcast('Jazz à FIP')
#   for episode in jaF.tracks:
#      print( f" {episode.name}")



#curl 'https://openapi.radiofrance.fr/v1/graphql' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://openapi.radiofrance.fr' -H 'x-token: 9a3e6731-041d-4dda-a754-f56e3ee0dd6b' --data-binary '{"query":"{\n  grid(\n    start: 1549868400\n    end: 1549881000\n    station: FRANCEINTER\n    includeTracks: false\n  ) {\n    ... on DiffusionStep {\n      id\n      diffusion {\n        id\n        title\n        standFirst\n        url\n        published_date\n        podcastEpisode {\n          id\n          title\n          url\n          playerUrl\n          created\n          duration\n        }\n      }\n    }\n    ... on TrackStep {\n      id\n      track {\n        id\n        title\n        albumTitle\n      }\n    }\n    ... on BlankStep {\n      id\n      title\n    }\n  }\n}\n"}' --compressed
  
#curl 'https://openapi.radiofrance.fr/v1/graphql' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' 
#-H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://openapi.radiofrance.fr' 
#-H 'x-token: 9a3e6731-041d-4dda-a754-f56e3ee0dd6b' --data-binary '{"query":"{\n  live(station: FIP) {\n\n    song {\n      id\n      start\n      end\n      track {\n        id\n        mainArtists\n        title\n        albumTitle\n        discNumber\n        trackNumber\n      }\n    }\n  }\n}\n"}' --compressed  