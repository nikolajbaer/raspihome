
class NoSuchSubzone(Exception): pass

class Zone(object):

    # DEBUG
    def index(self):
        return self.name
    index.exposed=True

    def __init__(self,id,name=None):
        self.id = id
        self.name = name or id
        self.subzones = {}
        self.sensors = {}
        self.actuators = {}

    def insert_subzone(self,z,path=[]):
        if not path:
            self.subzones[z.id] = z
            return
        p = path[0]
        if self.subzones.has_key(p):
            return self.subzones[p].insert_subzone(z,path[1:])
        raise NoSuchSubzone("Zone %s does not have a subzone %s"%(self.id,p))

class Sensor(object):
    def get_last_update(self):
        raise NotImplementedExecption("Return the date/time of your last update here")

    def initialize(self,cfg):
        # TODO init db?
        self.states=[]

    def read(self):
        raise NotImplementedException("Return your sensor state here")

    def update(self):
        pass

class Actuator(object):
    def initialize(self,cfg):
        pass

    def available_actions(self):
        return [] 

    def do(self,action,**kwargs):
        pass 


