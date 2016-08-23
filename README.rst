Kytos - python-openflow
=======================

|Openflow| |Tag| |Release| |Tests| |License|

*python-openflow* is a low level library to parse OpenFlow messages. If you want
to read an OpenFlow packet from an open socket or send a message to an OpenFlow
switch, this is your best friend. The main features are: high performance,
latest specification compliance, short learning curve and free software license.

This library is part of `Kytos <http://kytos.io>`_ project, a collaborative
project between SPRACE (from São Paulo State University, Unesp) and Caltech
(California Institute of Technology). *python-openflow*  was developed to be
used with *Kytos* controller, but feel free to use this simple and intuitive
library in another project with another controller.

Overview
--------

This is just an overview for you to check whether this project fits your needs.
For a more detailed documentation, please check the `python-openflow API
Reference Manual <http://docs.kytos.io/python-openflow/api-reference/>`_.

Usage
^^^^^

For example, see how it is easy to create a feature request message with this
library. You can use ipython3 to get the advantages of autocompletion:

.. The code in this section is replicated in docs/toc/usage.rst.

>>> from pyof.v0x01.controller2switch.features_request import FeaturesRequest
>>> request = FeaturesRequest(xid = 100)
>>> print(request.header.message_type)
Type.OFPT_FEATURES_REQUEST
>>> print(request.header.xid)
100

If you need to send this message via socket, call the ``pack()`` method to get
its binary representation:

.. code:: python

    >>> binary_msg = request.pack()

Installing
^^^^^^^^^^

The easiest way to install is using pip3 (pip for Python 3):

.. code:: shell

    sudo pip3 install python-openflow

Support
^^^^^^^

We are available in IRC and there is also a development mailing list. Details
are available in the full documentation.

Contributing
^^^^^^^^^^^^

Contributions are welcome either by creating issues in GitHub or in the form of
pull requests. Before, please, read the contribution and hacking guides in the
main documentation.

License
^^^^^^^

This software is under *MIT-License*. For more information please read
the ``LICENSE`` file.

.. |Openflow| image:: https://img.shields.io/badge/Openflow-1.0.0-brightgreen.svg
   :target: https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.0.0.pdf
.. |Tag| image:: https://img.shields.io/github/tag/kytos/python-openflow.svg
   :target: https://github.com/kytos/python-openflow/tags
.. |Release| image:: https://img.shields.io/github/release/kytos/python-openvpn.svg
   :target: https://github.com/kytos/python-openflow/releases
.. |Tests| image:: https://travis-ci.org/kytos/python-openflow.svg?branch=develop
   :target: https://github.com/kytos/python-openflow
.. |License| image:: https://img.shields.io/github/license/kytos/python-openflow.svg
   :target: https://github.com/kytos/python-openflow/blob/master/LICENSE
