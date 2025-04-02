import json

from model import *

class Radios(Artists):
    """ A radio is a track of a fake Album of a fake Artist named 'RADIOS' """
    def __init__( self, file:str='./public/radios.json'):
        with open( file) as json_data:
            list = filter( lambda x : x['type'] == 'radio',json.load(json_data))
            for r in list:
                radio = self.addTrack( r['file'], r['name'], 1, 0, 'RADIOS', r['name'], 0, '')
                radio.album.cover = r['cover']
            json_data.close()
     
 #    { "name" : "Fip", "file" : "http://direct.fipradio.fr/live/fip-hifi.aac", "cover":"FIP.jpg", "type": "radio"},
            

    def get_list( self):
        return self.get('RADIOS').albums

    def get_radio( self, filename:str)->Track|None:
        radioList = self.get('RADIOS').albums
        for r in radioList:
            if( r.tracks[0].file == filename):
                return r.tracks[0]
        return None


    def get_name( self, filename:str):
        radio = self.get_radio( filename)
        if ( radio == None):
            return ""
        else:
            return radio.name


    def get_cover( self, filename:str):
        radio = self.get_radio( filename)
        if ( radio == None):
            return ""
        else:
            return radio.album.cover

        
#RADIOS = Radios()
