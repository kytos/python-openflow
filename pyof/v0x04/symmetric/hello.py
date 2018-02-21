"""Defines Hello message."""

# System imports

from enum import IntEnum

from pyof.foundation.base import GenericMessage, GenericStruct
from pyof.foundation.basic_types import BinaryData, FixedTypeList, UBInt16
from pyof.foundation.exceptions import PackException
from pyof.v0x04.common.header import Header, Type

# Third-party imports

__all__ = ('Hello', 'HelloElemHeader', 'HelloElemType', 'ListOfHelloElements')

# Enums


class HelloElemType(IntEnum):
    """Hello element types."""

    #: Bitmap of version supported.
    OFPHET_VERSIONBITMAP = 1


# Classes


class HelloElemHeader(GenericStruct):
    """Common header for all Hello Elements."""

    element_type = UBInt16()
    length = UBInt16()
    content = BinaryData()

    def __init__(self, element_type=None, length=None, content=b''):
        """Create a HelloElemHeader with the optional parameters below.

        Args:
            element_type: One of OFPHET_*.
            length: Length in bytes of the element, including this header,
                excluding padding.
        """
        super().__init__()
        self.element_type = element_type
        self.length = length
        self.content = content

    def pack(self, value=None):
        """Update the length and pack the massege into binary data.

        Returns:
            bytes: A binary data that represents the Message.

        Raises:
            Exception: If there are validation errors.

        """
        if value is None:
            self.update_length()
            return super().pack()
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def update_length(self):
        """Update length attribute."""
        self.length = self.get_size()

    def unpack(self, buff=None, offset=0):
        """Unpack *buff* into this object.

        This method will convert a binary data into a readable value according
        to the attribute format.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.

        """
        length = UBInt16()
        length.unpack(buff, offset=offset+2)

        super().unpack(buff[:offset+length.value], offset)


class ListOfHelloElements(FixedTypeList):
    """List of Hello elements.

    Represented by instances of HelloElemHeader and used on Hello
    objects.
    """

    def __init__(self, items=None):
        """Create a ListOfHelloElements with the optional parameters below.

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
        """Create a Hello with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            elements: List of elements - 0 or more
        """
        super().__init__(xid)
        self.elements = elements
