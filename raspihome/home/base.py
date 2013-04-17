
class Space(object):
    def __init__(self,name):
        self.name = name
        self.spaces = {}
        self.sensors = {}
        self.actuators = {}

# CONSIDER: should everything be subspaces?

class Building(Space):
    def __init__(self,name):
        super(Building,self).__init__(name)
        self.rooms = {}

class Room(Space):
    def __init__(self,name):
        super(Room,self).__init__(name)
        self.name = name



class Sensor(object):
    def get_state(self):
        raise NotImplementedException("Return your sensor state here")

    def initialize(self,cfg):
        pass

    def read(self):
        return self.get_state()

    def update(self):
        pass


class Actuator(object):
    def initialize(self,cfg):
        pass


    def available_actions(self):
        return [] 

    def do(self,action,**kwargs):
        pass 


