import yaml,sys
from home.base import Zone
import cherrypy
from cherrypy.lib.static import serve_file
import json
import importlib

class Server(object):
    exposed = True

    def __init__(self,base_template="public/index.html"):
        self.facility = None
        self.zones = {} 
        self.panels = {}
        self.base_template = base_template

    def add_root_zone(self,name,zone):
        self.zones[name] = zone

    def add_panel(self,slug,panel):
        setattr(self,slug,panel)
        self.panels[slug] = panel
 
    def GET(self,*args):
        return open(self.base_template).read()

    def run(self):
        cherrypy.quickstart(self, config={'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})

def dynamic_import(path):
    module,klass = path.rsplit('.',1)
    Modu = importlib.import_module(module,klass)
    Klass = getattr(Modu,klass)
    return Klass

def panel_list_builder(o):
    panels = {}
    for p in o:
        P = dynamic_import(p["type"])
        panel = P(p["name"],p["config"])
        panels[p["slug"]] = panel
    return panels

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
    p.add_option("-p","--uiconfig",dest="uifile",help="UI Config File to load",default="my_ui.yaml")

    (options,args) = p.parse_args()

    try:
        cfg = yaml.load(open(options.cfgfile).read())
    except ValueError as e:
        print "Please provide a yaml configuration: ",e.message

    try:
        uicfg = yaml.load(open(options.uifile).read())
    except ValueError as e:
        print "Please provide a yaml UI configuration: ",e.message

    zones = zone_tree_builder(cfg)
    panels = panel_list_builder(uicfg)
    s=Server()    
    for z in zones.keys():
        s.add_root_zone(z,zones[z])
    for p in panels.keys():
        s.add_panel(p,panels[p])
    s.run()  

if __name__=="__main__":
    main()

