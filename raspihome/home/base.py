import urlparse

class NoSuchSubzone(Exception): pass
class ZoneURINotFound(Exception): pass

class Facility(object):
    def __init__(self,id,name=None):
        self.zones = {} 
        self.name = name
        self.id = id

    def add_root_zone(self,name,zone):
        self.zones[name] = zone


    def get(self,path,device=None):
        '''Gets by list of path slugs.'''
        if not self.zones.has_key(path[0]):
            return None
        return self.zones[path[0]].get(path[1:],device)

    def get_by_uri(self,uri):
        '''Parses Full or relative Zone URI to find appropriate Zone
        e.g. rhome://myhome/mylivingroom/#mantel_light 
        '''
        uri = urlparse.urlparse(uri)
        if uri.scheme and uri.scheme != ZONE_SCHEME:
            raise ValueError("Invalid Zone URI Scheme, expecting %s"%ZONE_SCHEME) 

        # TODO why does urlparse not do fragments without http?
        components = uri.path.split('#') 
        if uri.netloc and uri.netloc != self.id:
            # Raise an exception, as routing to facility should already be done by now
            raise ZoneURINotFound("Wrong Facility: you asked for %s, this is %s"%\
                                  (facility,self.id))

        return self.get(components[0].split('/'),\
                        len(components) > 1 and components[1] or None)

class Zone(object):
    def __init__(self,id,name=None):
        self.id = id
        self.name = name or id
        self.subzones = {}
        self.devices = {}

    def get(self,path,device):
        '''
        Recursively walk down zone tree to find matching path. 
        Returns None if not found
        '''
        if len(path) > 0:
            if self.subzones.has_key(path[0]):
                return self.subzones[path[0]].get(path[1:])
            else:
                return None
        # Otherwise, return device or zone
        if device:
            return self.devices.get(device,None)
        return self 

    def insert_subzone(self,z,path=[]):
        if not path:
            self.subzones[z.id] = z
            return
        p = path[0]
        if self.subzones.has_key(p):
            return self.subzones[p].insert_subzone(z,path[1:])
        raise NoSuchSubzone("Zone %s does not have a subzone %s"%(self.id,p))

class Device(object):
    '''Devices can represent both a sensor, actuator, or combined role'''
    def initialize(self,cfg):
        self.cfg = cfg

    def read(self):
        raise NotImplementedException("Return your sensor state here")

    def do(self,action,**kwargs):
        '''Runs action''' 
        raise NotImplementedException("Run action here")

    def available_actions(self):
        '''Return list of actions as a dictionary with format:
        {"action_name":{"param1":"<doc>","param2":"<doc>"}}
        '''
        return {} 

class Sensor(Device):
    '''Read-only device'''
    def available_actions(self):
        return {"update":{}} 

    def do_update(self):
        raise ToBeImplementedException("Sensors should run update here")

    def do(self,action,**kwargs):
        ''' Run no-op on all actions '''
        if action == "update":
            # CONSIDER: internal data store backend?
            return self.do_update()        

