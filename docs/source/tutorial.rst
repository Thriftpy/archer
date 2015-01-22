.. _tutorial:

tutorial
========

tutorial
--------

A minimal Archer application looks something like this::

    from archer import Archer
    app = Archer(__name__)

    @app.api('ping')
    def ping():
        return 'pong'


provided a hello.thrift file under your working directory,
define a service in the file::

    service PingPong {
        string ping(),
    }

So what did that code do?

1. First we imported the :class:`~archer.Archer` class.  An instance of this
   class will be our Thrift RPC server_side application.
2. Next we create an instance of this class. The first argument is the name of
   the application
3. We then use the :meth:`~archer.Archer.api` decorator to tell Archer what name
   defined in thrift file should trigger our function.
4. The function returns the message for ``ping`` RPC call, which is a string ``pong`` here
5. the service PingPong is defined in the hello.thrift file

Just save the python code as :file:`hello.py` (or something similar) and the
service definition in :file:`hello.thrift`, run it with your Python
interpreter.  Make sure to not call your application :file:`archer.py` because this
would conflict with Archer itself.

To run the application you can  use the :command:`archer` command::

    $ archer run
    * Running on 127.0.0.1:6000 in DEBUG mode


This launches a very simple built_in server, which is good enough for testing
but probably not what you want to use in production. For deployment options see
:ref:`deploying`.

Now run call the remote function you can also use the :command:`archer` command::

    $ archer call ping
    * pong

You should see that the string `pong` is returned


You can also run a client shell by::

    $ archer client
    >>> client.ping()

.. _public-server:

.. admonition:: Externally Visible Server

   you can make the server publicly available simply by adding
   ``--host=0.0.0.0`` to the command line::

       archer run --host=0.0.0.0

   This tells your operating system to listen on all public IPs.
