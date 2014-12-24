.. _api:

API
===

.. module:: archer

This part of the documentation covers all the interfaces of Archer.  For
parts where Archer depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Application Object
------------------

.. autoclass:: Archer
   :members:
   :inherited-members:

   .. automethod:: __init__




ApiMeta Object
--------------

.. currentmodule:: archer.app

.. autoclass:: ApiMeta
   :members:
   :inherited-members:

   .. automethod:: __init__

   .. attribute:: app

      The thrift app instance

   .. attribute:: name

      The api name

   .. attribute:: f

      The api function instance

   .. attribute:: args

      positional arguments

   .. attribute:: kwargs

      key_word arguments

   .. attribute:: start_time

      time when the api function is entered


ApiResultMeta
-------------

.. currentmodule:: archer.app

.. autoclass:: ApiResultMeta
   :members:
   :inherited-members:

   .. automethod:: __init__

   .. attribute:: result

      return value of the api

   .. attribute:: error

      exception instance raised from the api

   .. attribute:: end_time

      end time of the api call


Test Client
-----------

.. currentmodule:: archer.test

.. autoclass:: TestClient
   :members:

Fake Client
-----------

.. currentmodule:: archer.test

.. autoclass:: FakeClient
   :members:


.. _command_line_interface:

Command Line Interface
----------------------

.. automodule:: archer.cli
   :members:
   :undoc-members:

