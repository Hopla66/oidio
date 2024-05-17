#from model import *

class C2(object):
    def __init__(self, a):
        self.a = a
    def __str__(self):
        return "C2 object "+str(self.a)

"""
class Album2(object):
  def __init__( self, name:str, year:str, genre:str):
    self.name = name
    self.year = year
    self.genre = genre
    self.cover = ""

  def __str__(self):
    return "<Album2 "+self.name+">"        
"""

class C1(object):
    def __init__(self, a, c='', b:list[C2]=None):
        self.a = a
        if b == None:
            self.b = []
        else:
            self.b = b
        self.c = c
    
    def __str__(self):
        return "C1 object "+str(self.a)+"  "+str(self.b)        +"  :"+str(self.c)
    

x = C1( 'a',[C2('ppp')])
#x.b.append( Album2('ppp','1234','pipo'))
#x.b.append( C2('ppp'))
print(x)
y = C1('c')
print(y)

x.b.append( C2('ppx'))
print(x)
print(y)
"""
a1 = Artist('pipo')
print(a1)
a1.albums.append( Album('disk1','1923','disco'))
print(a1)
a2 = Artist('bingo')
print(a2)
"""