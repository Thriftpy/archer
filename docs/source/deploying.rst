.. _deploying:

deployment
==========

deployment
----------

The development Server is not suitable for production use,
we did not handle the thrift Protocol and Transport details instead of
providing a default one which is suitable for development.

`gunicorn_thrift <http://github.com/eleme/gunicorn_thrift>`_ is highly recommended
if you'd like to deploy an Archer application, as Archer is designed to work with
``gunicorn_thrift``.