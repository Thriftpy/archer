# -*- coding: utf-8 -*-
import logging
import os
import copy
import time
import functools
import errno
import imp

import thriftpy
from thriftpy.thrift import TProcessor

from .config import ConfigAttribute, import_string
from .event import before_api_call, after_api_call, tear_down_api_call
from ._server import run_simple
from .test import TestClient, FakeClient
from ._compat import PY2, iteritems, string_types


class ApiMeta(object):
    def __init__(self, app, name, f, args, kwargs):
        """
        meta object represent related info for an api

        :param app:  the archer app instance
        :param name: name of the api
        :param f:    function instance of the api
        :param args:  positional arguments
        :param kwargs:  keyword arguments

        """
        self.app = app
        self.name = name
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.start_time = time.time()


class ApiResultMeta(object):
    def __init__(self, result=None, error=None):
        """

        :param result: return value of api, if exception occurred, set None
        :param error: the exception instance raised in the api if any

        """
        self.result = result
        self.error = error
        self.end_time = time.time()


class Archer(object):
    debug = ConfigAttribute('DEBUG')
    testing = ConfigAttribute('TESTING')
    logger_name = ConfigAttribute('LOGGER_NAME')
    default_config = {
        'DEBUG': False,
        'TESTING': False,
        'LOGGER_NAME': None
    }

    def __init__(self, service_name, thrift_file=None, root_path=None,
            name=None):
        """
        initialize an archer application

        :param name:  app name
        :param thrift_file:  the thrift file to load by thriftpy, if not set
                             ,archer will automatically find a .thrift file
                             under root path
        :param service: service name of the thrift app
        :param root_path:  root path for file searching, default is pwd

        """
        self.root_path = root_path or os.getcwd()

        self.thrift_file = thrift_file or self._find_thrift_file()

        self.thrift = thriftpy.load(self.thrift_file)

        self.service_name = service_name
        self.service = getattr(self.thrift, service_name)
        self.name = name
        self.app = TProcessor(self.service, self)

        self.default_error_handler = None

        self.before_api_call_funcs = []
        self.after_api_call_funcs = []
        self.tear_down_api_funcs = []

        self.error_handlers = {}
        self.registered_errors = []

        self.api_map = {}
        self.api_meta_map = {}

        self.shell_context_processors = []

        self.config = copy.deepcopy(self.default_config)

        self.logger = logging.getLogger(self.logger_name)

    def _find_thrift_file(self):
        def _find_in_dir(path):
            for f in os.listdir(path):
                f = os.path.join(path, f)
                if f.endswith('.thrift'):
                    return f
                if os.path.isdir(f):
                    thrift_file = _find_in_dir(f)
                    if thrift_file:
                        return thrift_file

        return _find_in_dir(self.root_path)

    def run(self, host='127.0.0.1', port=6000, use_reloader=True, **options):
        run_simple(host, port, self, extra_files=[self.thrift_file],
                   use_reloader=use_reloader, **options)

    def make_shell_context(self):
        """Returns the shell context for an interactive shell for this
        application.  This runs all the registered shell context
        processors.

        """
        rv = {'app': self,
              'test_client': self.test_client,
              'fake_client': self.fake_client,
        }
        for processor in self.shell_context_processors:
            rv.update(processor())
        return rv

    def shell_context_processor(self, f):
        """registers a shell context processor function.
        A processor function is just a function that takes
        no arguments and return a dict object, which contains
        attributes that would be loaded in to the interactive shell
        e.g.::

            app = Archer('ServiceName')
            @app.shell_context_processor
            def redis_cli():
                import redis
                return {
                    'redis': redis.StrictRedis()
                }

        .. versionadded:: 0.1
           context

        """
        self.shell_context_processors.append(f)
        return f

    def register_default_error_handler(self, handler):
        self.default_error_handler = handler

    def errorhandler(self, error_type):
        def decorator(f):
            self.register_error_handler(error_type, f)
            return f

        return decorator

    def register_error_handler(self, error_type, f):
        """
        register an error_type on a given api function

        """
        assert error_type not in (Exception, BaseException), ValueError(
            "Please Register with `register_default_exc_handler`")
        if error_type in self.error_handlers:
            existing = self.error_handlers[error_type]
            raise KeyError("Handler (%s) already registered in %s" % (
                error_type, existing))
        self._append_error(error_type)
        self.error_handlers[error_type] = f

    def _append_error(self, new_exc):
        """
        append an exception_type to registered error types,
        ensure that the order is based on class's ``__mro__`` hierarchy

        """
        registered_errors = self.registered_errors

        for i, exc in enumerate(registered_errors):
            if new_exc is exc:
                registered_errors[i] = new_exc
                break
            elif issubclass(new_exc, exc):
                registered_errors.insert(i, new_exc)
                break
        else:
            registered_errors.append(new_exc)


    def before_api_call(self, f):
        """
        register a function which would always be called before
        an api function is called,
        the function would take one argument, which is an instance
        of :class:`~archer.app.ApiMeta`

        """
        self.before_api_call_funcs.append(f)
        return f

    def after_api_call(self, f):
        """
        register a function which would  be called after
        an api function is executed successfully
        the function would take one two arguments, the first one is
        an instance of :class:`ApiMeta` and the second one is an instance
        of :class:`~archer.app.ApiResultMeta`, same for :meth:`tear_down_api_call`.

        """
        self.after_api_call_funcs.append(f)
        return f

    def tear_down_api_call(self, f):
        """
        register a function which would always be called after
        an api is executed, no matter whether it returns normally or raise
        some error

        """
        self.tear_down_api_funcs.append(f)
        return f

    def api(self, name, **meta):
        """
        decorator used to register a thrift rpc api

        :param name:    api name
        :param meta: meta attributes would add to the app's api_meta_map
        :return: the original api function

        """

        def on_decorate(func):
            self.register_api(name, func, **meta)
            return func

        return on_decorate

    def register_api(self, name, f, **meta):
        if name in self.api_map:
            raise KeyError("Api_name(%s) already registered in %s" % (
                name, self.api_map[name].__module__
            ))
        self.api_map[name] = self._wrap_api(name, f)
        if PY2:
            self.api_map[name].__wrapped__ = f
        self.api_meta_map[name] = meta

    def _preprocess_api(self, api_meta):
        for handler in self.before_api_call_funcs:
            ret_val = handler(api_meta)

    def _postprocess_api(self, api_meta, result_meta):
        for handler in self.after_api_call_funcs:
            handler(api_meta, result_meta)

    def _tear_down_api(self, api_meta, result_meta):
        for handler in self.tear_down_api_funcs:
            handler(api_meta, result_meta)

    def _wrap_api(self, name, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            api_meta = ApiMeta(self, name, f, args, kwargs)
            before_api_call.notify(api_meta)
            self._preprocess_api(api_meta)
            try:
                ret_val = f(*args, **kwargs)
            except Exception as e:
                result_meta = ApiResultMeta(error=e)
                for exc_type in self.registered_errors:
                    handler = self.error_handlers[exc_type]
                    if isinstance(e, exc_type):
                        return handler(api_meta, result_meta)
                return self.handle_uncaught_exception(api_meta, result_meta)
            else:
                result_meta = ApiResultMeta(ret_val)
                after_api_call.notify(api_meta, result_meta)
                self._postprocess_api(api_meta, result_meta)
                return ret_val
            finally:
                tear_down_api_call.notify(api_meta, result_meta)
                self._tear_down_api(api_meta, result_meta)

        return wrapper

    def handle_uncaught_exception(self, api_meta, result_meta):
        if self.default_error_handler is not None:
            return self.default_error_handler(api_meta, result_meta)
        raise

    def processor(self, iprot, oprot):
        """
        delegate the processor method to the `app` attribute,
        which is an instance of :class:`thriftpy.thrift.TProcessor`.
        Make an Archer app compatible with the thrift_app definition in
        `gunicorn_thrift <http://github.com/eleme/gunicorn_thrift>`_
        """
        return self.app.processor(iprot, oprot)

    @property
    def test_client(self):
        """
        :return: an :class:`~archer.test.TestClient` instance

        """
        return TestClient(self)

    @property
    def fake_client(self):
        """
        :return: an :class:`~archer.test.FakeClient` instance

        """
        return FakeClient(self)

    def __getattr__(self, name):
        if name not in self.api_map:
            raise AttributeError(
                '''app don't have `{0}` attribute,
                   is it an api? if you mean an api,
                   this api `{0}` is not registered'''.format(name))
        return self.api_map[name]

    def config_from_envvar(self, variable_name, silent=False):
        """Loads a configuration from an environment variable pointing to
        a configuration file.  This is basically just a shortcut with nicer
        error messages for this line of code::

            app.config_from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])

        :param variable_name: name of the environment variable
        :param silent: set to ``True`` if you want silent failure for missing
                       files.
        :return: bool. ``True`` if able to load config, ``False`` otherwise.

        """
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)
        return self.from_pyfile(rv, silent=silent)

    def config_from_object(self, obj):
        """Updates the values from the given object.  An object can be of one
        of the following two types:

        -   a string: in this case the object with that name will be imported
        -   an actual object reference: that object is used directly

        Objects are usually either modules or classes.

        Just the uppercase variables in that object are stored in the config.
        Example usage::

            app.config_from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config_from_object(default_config)

        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_pyfile` and ideally from a location not within the
        package because the package might be installed system wide.

        :param obj: an import name or object

        """
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self.config[key] = getattr(obj, key)

    def config_from_pyfile(self, filename, silent=False):
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.

        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.

        """
        filename = os.path.join(self.root_path, filename)
        d = imp.new_module('config')
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                exec (
                    compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.config_from_object(d)
        return True
