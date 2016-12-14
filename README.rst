|Experimental| |Openflow| |Tag| |Release| |Pypi| |Tests| |License|

Overview
--------

*python-openflow* is a low level library to parse OpenFlow messages. If you
want to read an OpenFlow packet from an open socket or send a message to an
OpenFlow switch, this is your best friend. The main features are: high
performance, short learning curve and free software license.

This library is part of `Kytos <http://kytos.io>`_ project. *python-openflow*
was developed to be used with *Kytos* controller, but feel free to use this
simple and intuitive library in other projects.

This is just an overview for you to check whether this project fit your needs.
For a more detailed documentation, please check the :doc:`python-openflow API
Reference Manual <pyof>`.

Installing
^^^^^^^^^^

For now, you can install this package from source (if you have cloned this
repository) or via pip.

.. note:: We are improving this and soon you will be able to install from the
 major distros repositories.

From PyPI
=========

*python-openflow* is in PyPI, so you can easily install it via `pip3` (`pip`
for Python 3) or include this project in your `requirements.txt`. To install it
with `pip3`, run the following command:

.. code-block:: shell

   $ sudo pip3 install python-openflow

From source code
================

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

See how easy is the creation of a features request message with this library.
You can use ipython3 to get the advantages of autocompletion:

.. code-block:: python

    >>> from pyof.v0x01.controller2switch.features_request import FeaturesRequest
    >>> request = FeaturesRequest()
    >>> print(request.header.message_type)
    Type.OFPT_FEATURES_REQUEST

If you need to send this message via socket, call the ``pack()`` method to get
its binary representation that should be used to be sent throught the network:

.. code:: python3

    >>> binary_msg = request.pack()

Please note that this library do not send or receive messages via socket. You
have to create your own server to receive messages from switches. This library
only helps you to handle OpenFlow messages on a more pythonic way.

.. seealso::

    To see more examples, please visit our :doc:`examples/index` chapter.

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
