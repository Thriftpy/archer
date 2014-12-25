.. _foreword:

foreword
========

Why Thrift
----------

The Apache Thrift software framework, for scalable cross-language services
development, combines a software stack with a code generation engine to build
services that work efficiently and seamlessly between C++, Java, Python, PHP,
Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk, OCaml
and Delphi and other languages.

You just wrie a thrift file::

   thrift --gen <language> <Thrift filename>

after compiling for a given language, the corresponding SDK files are generated.

Why Thriftpy
------------

`Thriftpy`_ is a Python implementation of Thrift which generates SDK modules
dynamically when some thrift file is loaded, No SDK files any more, making
development procedure more fluently.


.. _Thriftpy: https://github.com/eleme/thriftpy/





