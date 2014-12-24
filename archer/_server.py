# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import threading
import time
import signal
from thriftpy.protocol import TBinaryProtocolFactory
from thriftpy.server import TThreadedServer
from thriftpy.thrift import TProcessor
from thriftpy.transport import TServerSocket, TBufferedTransportFactory

from .logger import log


_EXIT_RELOADER = 3


def restart_with_reloader(host, port):
    """Spawn a new Python interpreter with the same arguments as this one,
    but running the reloader thread.
    """
    log('info', 'Running on {}:{} in DEBUG mode'.format(host, port))
    while True:
        args = [sys.executable] + sys.argv
        new_environ = os.environ.copy()
        new_environ['archer.reload_loop'] = 'true'

        exit_code = subprocess.call(args, env=new_environ)
        if exit_code != _EXIT_RELOADER:
            return exit_code


def reloader_loop(extra_files=None, interval=1):
    """When this function is run from the main thread, it will force other
    threads to exit when any modules currently loaded change.

    :param extra_files: a list of additional files it should watch.
    :param interval: reload loop interval
    """
    from itertools import chain

    mtimes = {}
    while True:
        for filename in chain(_iter_module_files(), extra_files or ()):
            try:
                mtime = os.stat(filename).st_mtime
            except OSError:
                continue

            old_time = mtimes.get(filename)
            if old_time is None:
                mtimes[filename] = mtime
                continue
            elif mtime > old_time:
                log(
                    'info', ' * Detected change in %r, reloading' % filename)
                log('info', ' * Restarting with reloader')
                sys.exit(_EXIT_RELOADER)
        time.sleep(interval)


def _iter_module_files():
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            old = None
            while not os.path.isfile(filename):
                old = filename
                filename = os.path.dirname(filename)
                if filename == old:
                    break
            else:
                if filename[-4:] in ('.pyc', '.pyo'):
                    filename = filename[:-1]
                yield filename


def _make_server(app, host, port, daemon=True):
    processor = TProcessor(app.service, app)
    server_socket = TServerSocket(host=host, port=port)
    server = TThreadedServer(processor, server_socket,
                             iprot_factory=TBinaryProtocolFactory(),
                             itrans_factory=TBufferedTransportFactory(),
                             daemon=daemon)
    return server


def run_simple(host, port, app, extra_files=None, interval=1,
               use_reloader=True):
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    server = _make_server(app, host, port)
    if not use_reloader:
        log('info', 'server starting at {}:{}'.format(host, port))
        server.serve()

    if os.environ.get('archer.reload_loop') == 'true':
        t = threading.Thread(target=server.serve, args=())
        t.setDaemon(True)
        t.start()
        try:
            reloader_loop(extra_files, interval)
        except KeyboardInterrupt:
            return
    try:
        sys.exit(restart_with_reloader(host, port))
    except KeyboardInterrupt:
        pass
