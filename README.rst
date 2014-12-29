Archer
------

.. image:: http://img.shields.io/travis/eleme/archer/master.svg?style=flat
   :target: https://travis-ci.org/eleme/archer


Archer is a micro RPC framework inspired by `Flask` based on `Thrift`.

Archer is super easy to use
```````````````````````````

Save in a hello.py:

.. code:: python

   from archer import Archer
   app = Archer(__name__)

   @app.api('ping')
   def ping():
       return 'pong'


Save in a hello.thrift::

    service PingPong {
        string ping(),
    }

Archer would find the thrift file for you, and relying on `Thriftpy <https://thriftpy.readthedocs.org/en/latest/>`_
to generate code on the fly, and you don't need to specify the service name(here is
``PingPong``) in code as well.

And Easy to Setup
`````````````````


And run it:

.. code:: bash

   $ pip install Archer
   $ archer run
   * Running on 127.0.0.1:6000/

Archer would find the app instance to start a dev server, and reload it
when detecting changes on your python or thrift file.

Quick to get some feedback
``````````````````````````

Just run the command

.. code:: bash

   $ archer call ping

   * pong

Pretty cool, eh!

Links
`````

* `documentation <http://archer-thrift.readthedocs.org/en/latest/index.html>`_
