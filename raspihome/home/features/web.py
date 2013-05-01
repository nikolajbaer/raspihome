import cherrypy,json

class WebVisibleZone(object):
    exposed = True

    def __call__(self):
        return json.dumps({"name":self.name})

