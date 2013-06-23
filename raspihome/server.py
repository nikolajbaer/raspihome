import yaml,sys
from home.base import Zone,Facility
import cherrypy
from cherrypy.lib.static import serve_file
import json
import importlib

class Server(object):
    exposed = True

    def __init__(self,base_template="public/index.html"):
        self.facility = None
        self.panels = {}
        self.base_template = base_template

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

def panel_list_builder(o,f):
    panels = {}
    for p in o:
        P = dynamic_import(p["type"])
        panel = P(p["name"],p["config"],f)
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

def bootstrap(cfgfile,uifile,run_server=False):
    '''Build Facility from configfiles and init server
    Pass run_server=True to run the http server
    returns tuple of (Facility,Panels,Server)
    '''
    try:
        cfg = yaml.load(open(cfgfile).read())
    except ValueError as e:
        print "Please provide a yaml configuration: ",e.message
        return

    try:
        uicfg = yaml.load(open(uifile).read())
    except ValueError as e:
        print "Please provide a yaml UI configuration: ",e.message
        return

    zones = zone_tree_builder(cfg)
    f=Facility("my_facility","My Facility")
    panels = panel_list_builder(uicfg,f)
    s=Server()    
    for z in zones.keys():
        f.add_root_zone(z,zones[z])
    for p in panels.keys():
        s.add_panel(p,panels[p])
    if run_server:
        s.run()  

    return f,panels,s

def main():
    from optparse import OptionParser
    p = OptionParser()
    p.add_option("-c","--config",dest="cfgfile",help="Config File to load",default="my_home.yaml")
    p.add_option("-p","--uiconfig",dest="uifile",help="UI Config File to load",default="my_ui.yaml")

    (options,args) = p.parse_args()
    bootstrap(options.cfgfile,options.uifile,run_server=True)

if __name__=="__main__":
    main()

