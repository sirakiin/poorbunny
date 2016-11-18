from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse

import cherrypy

from bunny_commands import CommandFactory, ResultType


DEFAULT_PORT = 10086
DETAULT_CMD = 'g'


class PoorBunny(object):
    def __init__(self, commands=None):
        if not commands:
            commands = CommandFactory.export()
        self.commands = commands

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return self.do_command(*args, **kwargs)

    def do_command(self, *args, **kwargs):
        if args:
            method, margs = args[0].split(None, 1)
            if not method or method not in self.commands.cmd_list:
                method = DETAULT_CMD
                margs = args[0]
            cmd = self.commands.cmd_list.get(method, None)
            result, rtype = cmd(margs)
            if rtype == ResultType.REDIRECTION:
                raise cherrypy.HTTPRedirect(result)
            elif rtype == ResultType.CONTENT:
                # TODO: Add support to directly rendering content BEAUTIFULLY..
                return result


def start_bunny_server(bunny, port=None, errorlog=None, accesslog=None):
    if not port:
        port = DEFAULT_PORT
    cherrypy.server.socket_port = port
    cherrypy.config['log.error_file'] = errorlog
    cherrypy.config['log.access_file'] = accesslog
    return cherrypy.quickstart(bunny)


def parse_args():
    parser = argparse.ArgumentParser(description='Poor Bunny Server.')
    parser.add_argument('--port', type=int, required=False,
                        help='Port to run')
    parser.add_argument('--errorlog', type=str, required=False,
                        help='errorlog path')
    parser.add_argument('--accesslog', type=str, required=False,
                        help='accesslog path')
    return parser.parse_args()


def main():
    args = parse_args()
    start_bunny_server(PoorBunny(), args.port, args.errorlog, args.accesslog)


if __name__ == '__main__':
    main()

