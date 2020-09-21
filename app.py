import cherrypy
import os
from controller.controller_links import (GetRelatedLinks)


class App(object):
    # base class for all web services
    pass


conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.staticdir.dir': './docs'
    },
    '/links': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],

    },
    '/web': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './docs'
    }
}

webapp = App()
webapp.links = GetRelatedLinks()

if __name__ == '__main__':
    host_ip = "0.0.0.0"
    PORT = 9004
    cherrypy.tree.mount(webapp, '/', conf)
    cherrypy.engine.autoreload.match = r'^(?!settings).+'
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    cherrypy.config.update({'server.socket_host': host_ip,
                            'server.socket_port': PORT,
                            'log.screen': True
                            })

    cherrypy.engine.start()
    cherrypy.engine.block()
