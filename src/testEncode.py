import json

class Music(object):
    
    def __init__( self, name:str, value:str):
        self.name = name
        self.value = value

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__)
    
a = Music( 'a', 'x')
print( a.toJSON())
