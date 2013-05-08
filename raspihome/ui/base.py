import cherrypy,json,re

VALID_ACTION = re.compile("[a-zA-Z0-9_]{4,32}")

class Panel(object):
    exposed = True
    def __init__(self,name,cfg):
        self.name = name
        self.cfg = cfg
    
    def POST(self,action,**kwargs):
        # Actions should be alphanumeric with underscores from 4 - 32 characters long 
        if not VALID_ACTION.match(action):
            raise cherrypy.HTTPError(400) 
        if hasattr(self,"action_%s"%action):
            result = getattr(self,"action_%s"%action)(self,kwargs)
            cherrypy.response.headers["Content-Type"] = "application/json"
            return json.dumps(result)

    def get_data(self):
        raise NotImplementedException("Please subclass panel")    
 
    def GET(self):
        cherrypy.response.headers["Content-Type"] = "application/json"
        return json.dumps(self.get_data())

