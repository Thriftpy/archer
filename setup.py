# -*- coding: utf-8 -

"""
Archer
-----

Archer is a micro rpc framework inspired by Flask based on thrift
````````````

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

"""

import os

from setuptools import setup

from archer import __version__


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

fname = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(fname) as f:
    REQUIREMENTS = list(map(lambda l: l.strip(), f.readlines()))

py_modules = []

for root, folders, files in os.walk('archer'):
    for f in files:
        if f.endswith('.py'):
            full = os.path.join(root, f[:-3])
            parts = full.split(os.path.sep)
            modname = '.'.join(parts)
            py_modules.append(modname)

setup(
    name='archer',
    version=__version__,

    url='http://github.com/eleme/archer/',
    description='Thrift app the flask way',
    author='Wang Haowei',
    author_email='hwwangwang@gmail.com',
    license='MIT',

    classifiers=CLASSIFIERS,
    zip_safe=False,
    py_modules=py_modules,
    include_package_data=True,
    install_requires=[
        'click>=3.3',
        'thriftpy>=0.1.15'
    ],
    entry_points="""
    [console_scripts]
    archer=archer.cli:main
    """
)
