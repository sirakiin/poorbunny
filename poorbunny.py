from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import cherrypy
import socket


DEFAULT_PORT = 9090


class PoorBunny(object):
    def __init__(self, commands):
        self.commands = commands

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return self.do_command(args, kwargs)

    def do_command(self, *args, **kwargs):

        raise cherrypy.HTTPRedirect('http://www.github.com')


def start_bunny_server(bunny, port=DEFAULT_PORT, host=None, errorlog=None, accesslog=None):
    if not host:
        host = socket.gethostname()
    cherrypy.server.socket_port = port
    cherrypy.server.socket_host = host
    cherrypy.config['log.error_file'] = errorlog
    cherrypy.config['log.access_file'] = accesslog
    return cherrypy.quickstart(bunny)


def main():
    start_bunny_server(PoorBunny(None))


if __name__ == '__main__':
    main()










