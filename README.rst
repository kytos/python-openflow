|Experimental| |Openflow| |Tag| |Release| |Pypi| |Tests| |License|

Overview
========

*python-openflow* is a low level library to parse and create OpenFlow messages.
If you want to read an OpenFlow packet from an open socket or send a message to
an OpenFlow switch, this is your best friend. The main features are: high
performance, short learning curve and free software license.

This library is part of `Kytos <http://kytos.io>`_ project, but feel free to
use this simple and intuitive library in other projects.

.. attention::
   *python-openflow* does not perform I/O operations. To communicate with a
   switch, you can use, for example, `Kyco <http://docs.kytos.io/kyco>`_, the
   Kytos Controller.

A quick start follows for you to check whether this project fits your needs.
For a more detailed documentation, please check the
`python-openflow API Reference Manual <http://docs.kytos.io/python-openflow/pyof/>`_.

Quick Start
-----------

Installing
^^^^^^^^^^

For now, you can install this package from source (if you have cloned this
repository) or via pip. If you are a more experienced Python user, you can
also install it without root permissions.

.. note:: We are improving this and soon you will be able to install from the
 major distros' repositories.

From PyPI
"""""""""

*python-openflow* is in PyPI, so you can easily install it via `pip3` (`pip`
for Python 3) or include this project in your `requirements.txt`. To install it
with `pip3`, run the following command:

.. code-block:: shell

   $ sudo pip3 install python-openflow

From source code
""""""""""""""""

First you need to clone `python-openflow` repository:

.. code-block:: shell

   $ git clone https://github.com/kytos/python-openflow.git

After cloning, the installation process is done by standard `setuptools`
install procedure:

.. code-block:: shell

   $ cd python-openflow
   $ sudo python3 setup.py install

Basic Usage Example
^^^^^^^^^^^^^^^^^^^

See how it is easy to create a feature request message with this library.
You can use ipython3 to get the advantages of autocompletion:

.. code-block:: python

    >>> from pyof.v0x01.controller2switch.features_request import FeaturesRequest
    >>> request = FeaturesRequest()
    >>> print(request.header.message_type)
    Type.OFPT_FEATURES_REQUEST

If you need to send this message via socket, call the ``pack()`` method to get
its binary representation to be sent through the network:

.. code:: python

    >>> binary_msg = request.pack()
    >>> print(binary_msg)
    b"\x01\x05\x00\x08\x14\xad'\x8d"
    >>> # Use a controller (e.g. Kytos Controller) to send "binary_msg"

To parse a message, use ``unpack_message()``:

.. code:: python

   >>> from pyof.v0x01.common.utils import unpack_message
   >>> binary_msg = b"\x01\x05\x00\x08\x14\xad'\x8d"
   >>> msg = unpack_message(binary_msg)
   >>> print(msg.header.message_type)
   Type.OFPT_FEATURES_REQUEST

Please, note that this library do not send or receive messages via socket. You
have to create your own server to receive messages from switches. This library
only helps you to handle OpenFlow messages in a more pythonic way.
To communicate with switches, we also develop *Kyco*, the Kytos Controller.

.. hint::
   To see more examples, please visit our
   `Examples <http://docs.kytos.io/python-openflow/examples>`_ section.

.. |Experimental| image:: https://img.shields.io/badge/stability-experimental-orange.svg
.. |Openflow| image:: https://img.shields.io/badge/Openflow-1.0.0-brightgreen.svg
   :target: https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.0.0.pdf
.. |Tag| image:: https://img.shields.io/github/tag/kytos/python-openflow.svg
   :target: https://github.com/kytos/python-openflow/tags
.. |Release| image:: https://img.shields.io/github/release/kytos/python-openflow.svg
   :target: https://github.com/kytos/python-openflow/releases
.. |Pypi| image:: https://img.shields.io/pypi/v/python-openflow.svg
.. |Tests| image:: https://travis-ci.org/kytos/python-openflow.svg?branch=develop
   :target: https://travis-ci.org/kytos/python-openflow
.. |License| image:: https://img.shields.io/github/license/kytos/python-openflow.svg
   :target: https://github.com/kytos/python-openflow/blob/master/LICENSE
