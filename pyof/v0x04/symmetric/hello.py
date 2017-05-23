"""Defines Hello message."""

# System imports

from enum import IntEnum

from pyof.foundation.base import GenericMessage, GenericStruct
from pyof.foundation.basic_types import BinaryData, FixedTypeList, UBInt16
from pyof.v0x04.common.header import Header, Type

# Third-party imports

__all__ = ('Hello', 'HelloElemHeader', 'HelloElemType',
           'HelloElemVersionbitmap', 'ListOfHelloElements')

# Enums


class HelloElemType(IntEnum):
    """Hello element types."""

    #: Bitmap of version supported.
    OFPHET_VERSIONBITMAP = 1


# Classes


class HelloElemHeader(GenericStruct):
    """Common header for all Hello Elements."""

    element_type = UBInt16(enum_ref=HelloElemType)
    length = UBInt16()

    def __init__(self, element_type=None, length=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            element_type: One of OFPHET_*.
            length: Length in bytes of the element, including this header,
                excluding padding.
        """
        super().__init__()
        self.element_type = element_type
        self.length = length


class ListOfHelloElements(FixedTypeList):
    """List of Hello elements.

    Represented by instances of HelloElemHeader and used on Hello
    objects.
    """

    def __init__(self, items=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            items (HelloElemHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=HelloElemHeader, items=items)


class Hello(GenericMessage):
    """OpenFlow Hello Message OFPT_HELLO.

    This message includes zero or more hello elements having variable size.
    Unknown element types must be ignored/skipped, to allow for future
    extensions.
    """

    header = Header(message_type=Type.OFPT_HELLO)
    #: Hello element list
    elements = ListOfHelloElements()

    def __init__(self, xid=None, elements=None):
        """The constructor takes the parameters below.

        Args:
            xid (int): xid to be used on the message header.
            elements: List of elements - 0 or more
        """
        super().__init__(xid)
        self.elements = elements


class HelloElemVersionbitmap(HelloElemHeader):
    """Version bitmap Hello Element."""

    #: List of bitmaps - supported versions
    bitmaps = BinaryData()

    def __init__(self, bitmaps=b''):
        """The constructor just assigns parameters to object attributes.

        Args:
            bitmaps(BinaryData): A BinaryData with exactly (length - 4) bytes
                                 containing the bitmaps, then exactly
                                 (length + 7)/8*8 - (length) (between 0 and 7)
                                 bytes of all-zero bytes.
        """
        super().__init__(element_type=HelloElemType.OFPHET_VERSIONBITMAP,
                         length=None)
        self.bitmaps = bitmaps
