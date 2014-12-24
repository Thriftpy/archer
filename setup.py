import os

from setuptools import setup

from archer import __version__


readme = open('README.rst').read()

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
    long_description=readme,
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
