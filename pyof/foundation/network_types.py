"""Basic Network Types."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import BinaryData, HWAddress, UBInt8, UBInt16

__all__ = ('Ethernet',)


class Ethernet(GenericStruct):
    destination = HWAddress()
    source = HWAddress()
    type = UBInt16()
    data = BinaryData()

    def __init__(self, destination=None, source=None, type=None, data=b''):
        super().__init__()
        self.destination = destination
        self.source = source
        self.type = type
        self.data = data

    def __hash__(self):
        return hash(self.pack())

    def get_hash(self):
        return self.__hash__()
