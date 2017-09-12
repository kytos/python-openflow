"""General Unpack utils for python-openflow.

This package was moved from kytos/of_core for the purpose of creating a generic
method to perform package unpack independent of the OpenFlow version.
"""
from pyof import v0x01, v0x04
from pyof.foundation.exceptions import UnpackException

PYOF_VERSION_LIBS = {0x01: v0x01,
                     0x04: v0x04}


def validate_packet(packet):
    """Check if packet is valid OF packet.

    Raises:
        UnpackException: If the packet is invalid.
    """
    if not isinstance(packet, bytes):
        raise UnpackException('invalid packet')

    packet_length = len(packet)

    if packet_length < 8 or packet_length > 2**16:
        raise UnpackException('invalid packet')

    if packet_length != int.from_bytes(packet[2:4],
                                       byteorder='big'):
        raise UnpackException('invalid packet')

    version = packet[0]
    if version == 0 or version >= 128:
        raise UnpackException('invalid packet')


def unpack(packet):
    """Unpack the OpenFlow Packet and returns a message.

    Returns:
        GenericMessage: Message unpacked based on openflow packet.

    Raises:
        UnpackException: if the packet can't be unpacked.
    """
    validate_packet(packet)

    version = packet[0]
    try:
        pyof_lib = PYOF_VERSION_LIBS[version]
    except KeyError:
        raise UnpackException('Version not supported')

    try:
        header = pyof_lib.common.header.Header()
        header.unpack(packet[:header.get_size()])
        message = pyof_lib.common.utils.new_message_from_header(header)

        binary_data = packet[header.get_size():]
        binary_data_size = header.length - header.get_size()

        if binary_data and len(binary_data) == binary_data_size:
            message.unpack(binary_data)
        return message
    except (UnpackException, ValueError) as exception:
        raise UnpackException(exception)
