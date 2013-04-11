import cherrypy

class App(object):
    def index(self):
        return "Hello World!"
    index.exposed = True

cherrypy.config.update("raspihome.config")
cherrypy.quickstart(App())

