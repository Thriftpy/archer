.. _design:

Design Decisions in Archer
==========================

If you are curious why Archer does certain things the way it does and not
differently, this section is for you.  This should give you an idea about
some of the design decisions that may appear arbitrary and surprising at
first, especially in direct comparison with other frameworks.


The Explicit Application Object
-------------------------------

A thrift application based on gunicorn_thrift has to have one central
object that implements the actual application.  In Archer this is an
instance of the :class:`~archer.Archer` class.  Each Archer application has
to create an instance of this class itself.


That instance is your gunicorn_thrift application, you don't have to remember anything else.  If you
want to apply a gunicorn_thrift middleware, just wrap it and you're done (though
there are better ways to do that so that you do not lose the reference
to the application object :meth:`~archer.Archer.processor`).

Furthermore this design makes it possible to use a factory function to
create the application which is very helpful for unittesting and similar
things (:ref:`app-factories`).


Thread Locals
-------------

Unlike Flask, Archer doesn't use thread local objects, no magic globals
like `current_app`,  `request` in Flask.
We believe that things you can do with thread locals would exist a
better way to do without it, and decouple your code with these globals
means it would be easier to test and analyse, try to fire up a python
shell and type `import this`, one thing you can find is::

     "Explicit is better than implicit." --zen of Python

Say if we have an asynchronous rpc server instead, using thread locals
as globals would make no sense and break our application. Any way,
no thread locals leaves the door open.
We throw the ball to the end user to decide whether thread local would
be used in an archer app, for more information , refer to the article `GlobalState <https://code.djangoproject.com/wiki/GlobalState>`_.




What Archer is, What Archer is Not
----------------------------------


Archer will never have a database layer.  It will not have a form library
or anything else in that direction.  Archer itself just bridges to gunicorn_thrift
to implement a proper thrift application.
It also binds to a few common standard library packages such as logging.
Everything else is up for extensions.

Archer almost does nothing on the client side , as the client language
is depend on what you prefer, and how to use the connection is also
not predictable. So just implement the client side code the way you like
or just whatever to satisfy your need.

Why is this the case?  Because people have different preferences and
requirements and Archer could not meet those if it would force any of this
into the core.

The idea of Archer is to build a good foundation for all thrift applications.
Everything else is up to you.
