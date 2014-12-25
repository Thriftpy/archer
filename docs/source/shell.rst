.. _shell:

Working with the Shell
======================

One of the reasons everybody loves Python is the interactive shell.  It
basically allows you to execute Python commands in real time and
immediately get results back.  Archer itself does not come with an
interactive shell, because it does not require any specific setup upfront,
just import your application and start playing around.

There are however some handy helpers to make playing around in the shell a
more pleasant experience.  The main issue with interactive console
sessions is that you're not really triggering a real rpc call from  a client.

This is where some helper functions come in handy.  Keep in mind however
that these functions are not only there for interactive shell usage, but
also for unit testing and other situations that require a faked request
context.

Command Line Interface
----------------------

Thee recommended way to work with the shell is the
``archer shell`` command which does a lot of this automatically for you.
For instance the shell is automatically initialized with a loaded
application context. with globals ``app``, ``fake_client``, ``test_client``
already set at your hand::

>>> thrift_file = app.thrift_file
>>> test_client.ping()
>>> fake_client.ping()


You may want to add some other variables to the global scope of the shell
by using :meth:`~archer.Archer.shell_context_processor` method.

For more information see :ref:`cli`.




