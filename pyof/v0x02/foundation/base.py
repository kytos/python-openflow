"""Base and fundamental classes used all over the library.

Besides classes, several constants are defined here. We designed
python-openflow in a manner to make it easy to create new messages and OpenFlow
structs. You can realize that when you see a message class definition.

A **struct** here is a group of basic attributes and/or struct attributes (i.e.
:class:`~.common.header.Header`). A **message** here is like a struct, but all
messages have a header attribute (i.e.
:class:`~.asynchronous.packet_in.PacketIn`).

The main classes of this module are :class:`GenericStruct`,
:class:`GenericMessage`, :class:`GenericBitMask` and :class:`GenericType`.
These classes are used in all parts of this library.
"""
from pyof.v0x01.foundation.base import (GenericBitMask, GenericMessage,
                                        GenericStruct, GenericType,
                                        MetaBitMask, MetaStruct)
