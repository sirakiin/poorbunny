from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from functools import wraps
from requests.models import Request

PYTHON2_REF = 'https://docs.python.org/2/search.html'
PYTHON3_REF = 'https://docs.python.org/3/search.html'
GOOGLE_SEARCH = 'https://www.google.com/search'
GOOGLE_MAIL = 'https://mail.google.com/mail/u/'
DEALMOON = 'http://cn.dealmoon.com/top/'
CPLUSPLUS = 'http://www.cplusplus.com/search.do'


class ResultType(object):
    REDIRECTION = 'redirection'
    CONTENT = 'content'


class BunnyCommands(object):
    def __init__(self, cmd_list):
        self.cmd_list = cmd_list


class CommandFactory(object):
    REGISTERED_COMMANDS = {}

    @classmethod
    def export(cls, cmd_list=None):
        # TODO: Use cmd_list to have configurable command list
        # commands = [x for x in cls.REGISTERED_COMMANDS if x.__name__ in cmd_list]
        commands = cls.REGISTERED_COMMANDS
        return BunnyCommands(commands)


def register_command(cmd):
    CommandFactory.REGISTERED_COMMANDS[cmd.__name__] = cmd
    return cmd


def register_redirection_command(cmd):
    @wraps(cmd)
    def wrapped(*args, **kwargs):
        ret = cmd(*args, **kwargs)
        return ret, ResultType.REDIRECTION
    register_command(wrapped)
    return wrapped


def register_content_command(cmd):
    @wraps(cmd)
    def wrapped(*args, **kwargs):
        ret = cmd(*args, **kwargs)
        return ret, ResultType.CONTENT
    register_command(wrapped)
    return wrapped


# TODO: separate core functions apart from additional functions


@register_redirection_command
def py(arg):
    # TODO: Implement feeling lucky search
    payload = {'q': arg}
    return Request(url=PYTHON2_REF, params=payload).prepare().url


@register_redirection_command
def py3(arg):
    # TODO: Implement feeling lucky search
    payload = {'q': arg}
    return Request(url=PYTHON3_REF, params=payload).prepare().url


@register_redirection_command
def g(arg):
    payload = {'q': arg}
    return Request(url=GOOGLE_SEARCH, params=payload).prepare().url


@register_redirection_command
def glucky(arg):
    payload = {'q': arg}
    return Request(url=GOOGLE_SEARCH, params=payload).prepare().url + '&btnI'


@register_redirection_command
def deal(arg):
    return DEALMOON + (arg if arg else '')


@register_redirection_command
def gmail(arg):
    """
    Go to gmail, with account number arg
    :param arg: Account #
    :return:
    """
    if not arg:
        return GOOGLE_MAIL
    try:
        account_num, search_content = arg.split(None, 1)
    except ValueError:
        account_num, search_content = arg, None
    return GOOGLE_MAIL + account_num + ('/#search/' + search_content) if search_content else ''


@register_content_command
def _debug(*args, **kwargs):
    try:
        method, margs = args[0].split(None, 1)
        margs = [margs] + list(args[1:])
    except ValueError:
        method = args[0]
        margs = args[1:]
    real_cmd = CommandFactory.REGISTERED_COMMANDS.get(method, None)
    if not callable(real_cmd):
        return 'Error, {method} not found!'.format(method=method)
    else:
        result, _ = real_cmd(*margs, **kwargs)
        return "<code><b>poorbunny</b><br/> DEBUG: redirect to <a href='{url}'>{url}</a></code>".format(url=result)


@register_redirection_command
def cpp(arg):
    payload = {'q': arg}
    return Request(url=CPLUSPLUS, params=payload).prepare().url