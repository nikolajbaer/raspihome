from home.base import *

def init():
    b = Building("home")
    b.rooms["living"] = Room("living")    
    b.rooms["kitchen"] = Room("kitchen")
    b.rooms["office"] = Room("office")
    b.rooms["kids bed"] = Room("kids")
    b.rooms["master bed"] = Room("master")
    b.rooms["kids bath"] = Room("main bath")
    b.rooms["master bath"] = Room("master bath")

    #b.sensors["net"] =  

if __name__ == "__main__":
    init()

