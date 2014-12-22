# -*- coding: utf-8 -*-


import sys

import click

from ._compat import iteritems


class NoAppException(click.UsageError):
    """Raised if an application cannot be found or loaded."""


def locate_app(app_id):
    """Attempts to locate the application."""

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
    from . import Archer

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


class Config(object):
    def __init__(self):
        self.app = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--app', help='app to start')
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
    import code

    app = locate_app(config.app)
    with app.app_context():
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
            from IPython.config.loader import Config

            cfg = Config()
            IPython.embed(config=cfg, user_ns=ctx, banner1=banner)
        except ImportError:
            code.interact(banner=banner, local=ctx)