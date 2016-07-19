Introduction
============

Our main goal is to make the development of OpenFlow applications easy and
straightforward. This library is the foundation for the development of any
OpenFlow application.

If you have read the OpenFlow specification, the learning curve for using this
library will be minimal. We tried to keep it very close to the specs regarding
class names and attributes.

Source code structure
---------------------

This project is packed as a python package (``python-openflow``), and contains
the following directory structure:

* ``pyof/``: contains all the implemented versions of the OpenFlow Protocol
  Parser:

  * Each version has its own folder;
  * Each version inherits from previous version using OOP techniques. So
    when a new protocol version is released, we implement only the changes and
    new code;

* ``docs/``: We use sphinx_ to document our code, including this page that you
  are reading. On this directory we save only the ``.rst`` files and
  documentation source code;

* ``tests/``: Here we use unit tests to keep our code working with automatic
  checks. Each OpenFlow version has its own unittest suit below its directory;

* ``raw/``: raw (binary) OpenFlow Messages, dumped with tcpdump_ used for
  testing purposes.

Main Highlights
---------------

Speed focused
~~~~~~~~~~~~~

We keep the word *performance* in mind since the beginning of the development.
Also, as computer scientists, we will always try to get the best performance by
using the most suitable algorithms.

Some of our developers participated in several demonstrations involving tests
with high-speed networks (~1 terabit/s), some even involving data transfers
from/to CERN.

Always updated
~~~~~~~~~~~~~~

To avoid code repetition this project utilizes an incremental architecture.

This means that the first version (1.0.0 = v0x01) was coded from the full
OpenFlow 1.0.2 Protocol. The 1.1 version (v0x02) imports the 1.0 version and
then do the necessary changes to make it compatible with the OpenFlow 1.1.0
Protocol, and the next version follows the same logic.

Using incremental code makes the implementation of new versions of OpenFlow
protocol faster. Our main goal is to follow the specifications since the very
beginning.

Easy to learn
~~~~~~~~~~~~~

Python is an easy language to learn and we aim at writing code in a "pythonic
way". We also provide a well documented API. Thus, learning to make your
controller using this library is a trivial task.

Born to be free
~~~~~~~~~~~~~~~

OpenFlow was born with a simple idea: make your network more vendor agnostic
and we like that!

We are advocates and supporters of free software and we believe that the more
eyes observe the code, the better it will be. This project can receive support
from many vendors, but will never follow a particular vendor direction.

*python-openflow* will always be free software.


.. _sphinx: http://sphinx.pocoo.org/
.. _tcpdump: http://www.tcpdump.org/
