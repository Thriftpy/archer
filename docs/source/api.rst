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

   .. automethod:: __init__

   .. attribute:: root_path

   .. attribute:: thrift_file

   .. attribute:: thrift

   .. attribute:: service

   .. attribute:: name

   .. attribute:: app

   .. attribute:: default_error_handler

   .. attribute:: before_api_call_funcs

   .. attribute:: after_api_call_funcs

   .. attribute:: tear_down_api_funcs

   .. attribute:: error_handlers

   .. attribute:: registered_errors

   .. attribute:: api_map

   .. attribute:: api_meta_map

   .. attribute:: shell_context_processors

   .. attribute:: config

   .. attribute:: logger


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

.. module:: archer.test

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

.. module:: archer.cli

.. data:: call

.. data:: shell

.. data:: run


