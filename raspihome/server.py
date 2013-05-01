import yaml,sys
from home.base import Zone
import cherrypy
import json

class Server(object):
    def __init__(self,web_port=8000):
        self.web_port = web_port
        self.facility = None

    def add_zone(self,name,zone):
        # CONSIDER is this too dangerous?
        pass
 
    def index(self,*args):
        cherrypy.response.headers["Content-Type"] = "application/json"
        return json.dumps(args)
    index.exposed = True

    def run(self):
        # Boot Cherrypy server
        cherrypy.quickstart(self)

def zone_tree_builder(o):
    zones = {} 
    for z in o:
        if z.has_key("features"):
            # TODO if has features, generate a new mixin class on the fly </guitar solo>
            pass
        zone = Zone(z["id"],z.get("name",None))
        if z.has_key("path"):
            path = z["path"].split("/")
            zones[path[0]].insert_subzone(zone,path[1:])
        else:
            zones[z["id"]] = zone
        # TODO add sensors
        # TODO add actuators
    return zones

def main():
    from optparse import OptionParser
    p = OptionParser()
    p.add_option("-c","--config",dest="cfgfile",help="Config File to load",default="my_home.yaml")

    (options,args) = p.parse_args()

    try:
        cfg = yaml.load(open(options.cfgfile).read())
    except ValueError as e:
        print "Please provide a yaml configuration: ",e.message

    zones = zone_tree_builder(cfg)
    s=Server()    
    for z in zones.keys():
        s.add_zone(z,zones[z])
    s.run()  

if __name__=="__main__":
    main()

