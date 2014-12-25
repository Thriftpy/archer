.. _server:

Development Server
==================

.. currentmodule:: archer

It's quite easy to fire up a development server by using the :command:`archer`
    command line utility with :meth:`Archer.run` method.

Command Line
------------

The :command:`archer` command line script (:ref:`cli`) is strongly recommended for
development because it provides a superior reload experience due to how it
loads the application.  The basic usage is like this::

    $ archer --app my_application  run

This will enable the reloader and then start the server on
*http://localhost:6000/*.

If you put your app instance in a python file or a ``__init__.py`` file in
some directory under the :attr:`~archer.Archer.root_path`,
archer will find the app for you automatically. In such cases, just::

   $ archer run

And the server would start the same way. Super easy!


In Code
-------

The alternative way to start the application is through the
:meth:`Archer.run` method.  This will immediately launch a local server
exactly the same way the :command:`archer` script does.

Example::

    if __name__ == '__main__':
        app.run()


client
------

Archer also provide the :command:`archer call` to easy test a api without
any coding::

    $ archer --app my_application  call api_name param1,param2....

if you'd like archer find the app for you, just::

   $ archer call api_name param1, param2...

And if everything is ok, the terminal would echo the return value
of this api, or just the string ``OK`` if nothing is returned.

parameters are just separated by comma or whitespace, so
``a b c d`` and ``a,b,c,d`` are both ok.

Archer would handle the parameter type, so `123` would convert to int type.
You can specify the type using ``:`` after a parameter, like ``123:string``,
so that Archer would known that  you want 123 to be a string instead of int.

.. admonition:: Non built_in type

    Customized types are not supported, as :command:`call` command is just
    for quickly getting some feedback of an api, You need more complicated test
    cases to ensure your api work correctly, so don't rely heavily on this
    command.

