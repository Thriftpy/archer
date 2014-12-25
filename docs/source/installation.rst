.. _installation:

Installation
============

Archer depends on some external libraries, like `Thriftpy
<https://github.com/eleme/thriftpy/>`_ and `Click <https://github.com/mitsuhiko/click/>`_.
Thriftpy is an  Thrift interface definition language interpreter written in
Python which would load a thrift file and generate SDK module on the fly,
saving you the time for compiling the thrift file by hand.

Click is a Python package for creating beautiful command line interfaces
in a composable way with as little code as necessary.

So how do you get all that on your computer quickly?  There are many ways you
could do that, but the most kick-ass method is virtualenv, so let's have a look
at that first.

You will need Python 2.6 or newer to get started, so be sure to have an
up-to-date Python 2.x installation.  Python 3.x would also be OK.

.. _virtualenv:

virtualenv
----------

Virtualenv is probably what you want to use during development, and if you have
shell access to your production machines, you'll probably want to use it there,
too.

What problem does virtualenv solve?  If you like Python as much as I do,
chances are you want to use it for other projects besides Archer-based RPC
applications.  But the more projects you have, the more likely it is that you
will be working with different versions of Python itself, or at least different
versions of Python libraries.  Let's face it: quite often libraries break
backwards compatibility, and it's unlikely that any serious application will
have zero dependencies.  So what do you do if two or more of your projects have
conflicting dependencies?

Virtualenv to the rescue!  Virtualenv enables multiple side-by-side
installations of Python, one for each project.  It doesn't actually install
separate copies of Python, but it does provide a clever way to keep different
project environments isolated.  Let's see how virtualenv works.

If you are on Mac OS X or Linux, chances are that one of the following two
commands will work for you::

    $ sudo easy_install virtualenv

or even better::

    $ sudo pip install virtualenv

One of these will probably install virtualenv on your system.  Maybe it's even
in your package manager.  If you use Ubuntu, try::

    $ sudo apt-get install python-virtualenv


Once you have virtualenv installed, just fire up a shell and create
your own environment.  I usually create a project folder and a :file:`venv`
folder within::

    $ mkdir myproject
    $ cd myproject
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools, pip............done.

Now, whenever you want to work on a project, you only have to activate the
corresponding environment.  On OS X and Linux, do the following::

    $ . venv/bin/activate

If you are a Windows user, the following command is for you::

    $ venv\scripts\activate

Either way, you should now be using your virtualenv (notice how the prompt of
your shell has changed to show the active environment).

And if you want to go back to the real world, use the following command::

    $ deactivate

After doing this, the prompt of your shell should be as familiar as before.

Now, let's move on. Enter the following command to get Archer activated in your
virtualenv::

    $ pip install Archer

A few seconds later and you are good to go.


System-Wide Installation
------------------------

This is possible as well, though I do not recommend it.  Just run
:command:`pip` with root privileges::

    $ sudo pip install Archer

(On Windows systems, run it in a command-prompt window with administrator
privileges, and leave out :command:`sudo`.)


Living on the Edge
------------------

If you want to work with the latest version of Archer, there are two ways: you
can either let :command:`pip` pull in the development version, or you can tell
it to operate on a git checkout.  Either way, virtualenv is recommended.

Get the git checkout in a new virtualenv and run in development mode::

    $ git clone http://github.com/eleme/archer.git
    Initialized empty Git repository in ~/dev/archer/.git/
    $ cd archer
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools, pip............done.
    $ . venv/bin/activate
    $ python setup.py develop
    ...
    Finished processing dependencies for Archer

This will pull in the dependencies and activate the git head as the current
version inside the virtualenv.  Then all you have to do is run ``git pull
origin`` to update to the latest version.
