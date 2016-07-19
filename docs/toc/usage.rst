Usage
=====

The main goal of this library is to provide a very simple and intuitive syntax
to parse OpenFlow packets. As we support multiple OpenFlow versions, you need to
be specific on which version to import.

Parsing a message
-----------------

Creating a message
------------------
For example, let's create a feature request message. Tip: you can use ipython3
for autocompletion:

.. The code in this section is replicated in README.rst.

>>> from pyof.v0x01.controller2switch.features_request import FeaturesRequest
>>> request = FeaturesRequest(xid = 100)
>>> print(request.header.message_type)
Type.OFPT_FEATURES_REQUEST
>>> print(request.header.xid)
100

A simple controller example
---------------------------
