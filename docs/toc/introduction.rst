Introduction
============

Our main goal is to make the development of OpenFlow applications easy and
straightforward. This library is the foundation for the development of any
OpenFlow application.

If you have read the OpenFlow specification, the learning curve for using this
library will be minimal. We tried to keep very close to the specs regarding
class names and attributes.

Source code structure
---------------------

This project is packed as a python package (``python-openflow``), and contains
the following directory structure:

* ``pyof/``: contains all the implemented versions of the OpenFlow Protocol
  Parser. Each version is under its own folder:

  * Each version is inside its own directory

  * Each version inherits from previous version using POO techniques. So
    when a new protocol version is released, we implement only the changes and
    new code.

* ``docs/``: We use sphinx_ to document our code, including this page that you
  are reading. On this directory we save only the ``.rst`` files and
  documentation source code.

* ``tests/``: Here we use unit tests to keep our code working with automatic
  checks. Each OpenFlow version has its own unittest suit on the this directory

* ``raw/``: raw (binary) OpenFlow Messages, dumped with tcpdump_ used for tests
  purposes

Main highlights
---------------

Speed focused
~~~~~~~~~~~~~

We keep the word performance in mind since the beginning of the development.
Also, as computer scientists we will always try to get the best performance by
using the most suitable algorithm.

Some developers participated in several demonstrations involving tests with
high-speed networks (~ 1 terabit/s), some even involving data transfers from/to
CERN.

Always updated
~~~~~~~~~~~~~~

To avoid code repetition this project utilizes an incremental architecture.

This means that the first version (1.0.0 = v0x01) was fully coded from the
OpenFlow 1.0.0 Protocol. The 1.1 version (v0x02) imports the 1.0 version and
then do the necessary changes to make it compatible with the OpenFlow 1.1.0
Protocol, and the next version follows the same logic.

Using incremental code makes the implementation of new versions of OpenFlow
protocol faster. Yes, we are at initial stages of development, but our main goal
is always follow the specs.

Easy to learn
~~~~~~~~~~~~~

We try to code in a "pythonic way" always. We also have a well documented API.
Learn to make your controller using this library is a trivial task.

Born to be free
~~~~~~~~~~~~~~~

OpenFlow was born with a simple idea: make your network more vendor agnostic and
we like that!

We are advocates and supporters of free software and we believe that the more
eyes observe a certain code, a better code will be generated. This project can
receive support of many vendors, but never will follow a particular vendor
direction.

We always will keep this code open.

.. _sphinx: http://sphinx.pocoo.org/
.. _tcpdump: http://www.tcpdump.org/
