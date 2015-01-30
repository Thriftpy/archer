# -*- coding: utf-8 -*-
import os

import sys
sys.path.append('.')
import importlib
import traceback

import click
import re

from ._compat import iteritems
from .helper import make_client



class NoAppException(click.UsageError):
    """Raised if an application cannot be found or loaded."""


def locate_app(app_id):
    """Attempts to locate the application."""

    if app_id is None:
        return find_app_in_cwd()
    if ':' in app_id:
        module, app_obj = app_id.split(':', 1)
    else:
        module = app_id
        app_obj = None

    __import__(module)
    mod = sys.modules[module]
    if app_obj is None:
        app = find_best_app(mod)
    else:
        app = getattr(mod, app_obj, None)
        if app is None:
            raise RuntimeError('Failed to find application in module "%s"'
                               % module)

    return app


def find_best_app(module):
    """Given a module instance this tries to find the best possible
    application in the module or raises an exception.
    """
    from .app import Archer

    for attr_name in 'app', 'application':
        app = getattr(module, attr_name, None)
        if app is not None and isinstance(app, Archer):
            return app

    # Otherwise find the only object that is a Archer instance.
    matches = [v for k, v in iteritems(module.__dict__)
               if isinstance(v, Archer)]

    if len(matches) == 1:
        return matches[0]
    raise NoAppException('Failed to find application in module "%s".  Are '
                         'you sure it contains a Archer application? '
                         % module.__name__)


def find_app_in_cwd():
    # from examples import app
    # return app
    trial_modules = []
    for f in os.listdir(os.getcwd()):
        if f.endswith('.py') and f not in ('setup.py',):
            trial_modules.append(importlib.import_module(f[:-3]))
        if os.path.isdir(f):
            # import pdb
            # pdb.set_trace()
            fs = os.listdir(f)
            if '__init__.py' in fs:
                trial_modules.append(importlib.import_module(f))
    for module in trial_modules:
        try:
            return find_best_app(module)
        except NoAppException:
            continue
    raise NoAppException


class Config(object):
    def __init__(self):
        self.app = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--app', default=None)
@pass_config
def main(config, app):
    config.app = app


@main.command('run', short_help='Runs a development server.')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=6000,
              help='The port to bind to.')
@click.option('--reload/--no-reload', default=True,
              help='Enable or disable the reloader.  By default the reloader '
)
@pass_config
def run(config, host, port, reload):
    app = locate_app(config.app)
    app.run(host, port, use_reloader=reload)


@main.command('shell', short_help='Runs a shell in the app context.')
@pass_config
def shell(config):
    app = locate_app(config.app)
    banner = 'Python %s on %s\nApp: %s%s\n' % (
        sys.version,
        sys.platform,
        app.name,
        app.debug and ' [debug]' or '',
    )
    ctx = {'a': 123}

    ctx.update(app.make_shell_context())

    sys.path.append('.')
    try:
        import IPython

        IPython.embed(user_ns=ctx, banner1=banner)
    except ImportError:
        import code

        code.interact(banner=banner, local=ctx)


@main.command('call', short_help='Runs a client')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=6000,
              help='The port to bind to.')
@click.argument('api')
@click.argument('arguments', required=False, nargs=-1)
@pass_config
def call(config, host, port, api, arguments):
    """
    call an api with given arguments, this is a command for quickly
    testing if a api is working, it's better to write test case
    warning: arguments of customized thrift type not supported yet
    """
    arguments = ' '.join(arguments)
    if ',' in arguments:
        sep = '\s*,\s*'
    else:
        sep = '\s+'
    args = re.split(sep, arguments.strip())
    params = []
    for arg in args:
        if ':' in arg:
            value, type_ = arg.split(':')

            type_ = getattr(sys.modules['__builtin__'], type_)
            value = type_(value)
            params.append(value)
        else:
            try:
                params.append(int(arg))
            except ValueError:
                params.append(arg)

    app = locate_app(config.app)
    client = make_client(app.service, host, port)
    try:
        result = getattr(client, api)(*params)
        if result is not None:
            click.echo(result)
        else:
            click.echo('OK')
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        click.echo(traceback.format_exc(exc_traceback))


@main.command('client', short_help='Runs a client shell')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=6000,
              help='The port to bind to.')
@pass_config
def client(config, host, port):
    from .helper import make_client
    app = locate_app(config.app)
    client = make_client(app.service, host, port)
    banner = 'Python %s on %s\nApp: %s%s\n' % (
        sys.version,
        sys.platform,
        app.name,
        app.debug and ' [debug]' or '',
    )
    ctx = {'client': client}
    ctx.update(app.make_shell_context())
    sys.path.append('.')
    try:
        import IPython

        IPython.embed(user_ns=ctx, banner1=banner)
    except ImportError:
        import code

        code.interact(banner=banner, local=ctx)
