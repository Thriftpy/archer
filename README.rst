Archer
------

Archer is a micro rpc framework inspired by Flask based on thrift

Archer is super easy to use
```````````````````````````

Save in a hello.py:

.. code:: python

   from archer import Archer
   app = Archer(__name__)

   @app.api('ping')
   def ping():
       return 'pong'

   if __name__ == "__main__":
       app.run()


Save in a hello.thrift::

    service PingPong {
        string ping(),
    }

Archer would find the thrift file for you, and relying on ``Thriftpy`` to
generate code on the fly.

And Easy to Setup
`````````````````


And run it:

.. code:: bash

   $ pip install Archer
   $ python hello.py
   * Running on 127.0.0.1:6000/

Links
`````

* `documentation <http://archer-thrift.readthedocs.org/en/latest/index.html>`_