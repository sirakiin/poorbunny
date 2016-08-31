from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from requests.models import Request

PYTHON2_REF = 'https://docs.python.org/2/search.html'


class ResultType(object):
    REDIRECTION = 'redirection'
    CONTENT = 'content'


class BunnyCommands(object):
    def __init__(self, cmd_list):
        self.cmd_list = cmd_list


class CommandFactory(object):
    REGISTERED_COMMANDS = set()

    @classmethod
    def export(cls, cmd_list):
        # TODO: Use cmd_list to have configurable command list
        # commands = [x for x in cls.REGISTERED_COMMANDS if x.__name__ in cmd_list]
        commands = cls.REGISTERED_COMMANDS
        return BunnyCommands(commands)


def register_command(cmd):
    CommandFactory.REGISTERED_COMMANDS.add(cmd)
    return cmd


@register_command
def py(arg):
    payload = {'q': arg}
    return Request(url=PYTHON2_REF, params=payload).prepare().url




