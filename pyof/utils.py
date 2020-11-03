"""General Unpack utils for python-openflow.

This package was moved from kytos/of_core for the purpose of creating a generic
method to perform package unpack independent of the OpenFlow version.
"""
from pyof import v0x01, v0x04
from pyof.foundation.exceptions import UnpackException
from pyof.v0x01.common import utils as u_v0x01  # pylint: disable=unused-import
from pyof.v0x04.common import utils as u_v0x04  # pylint: disable=unused-import

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

    if packet_length != int.from_bytes(packet[2:4], byteorder='big'):
        raise UnpackException('invalid packet')

    version = packet[0]
    if version == 0 or version >= 128:
        raise UnpackException('invalid packet')


def unpack(packet):
    """Unpack the OpenFlow Packet and returns a message.

    Args:
        packet: buffer with the openflow packet.

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
        message = pyof_lib.common.utils.unpack_message(packet)
        return message
    except (UnpackException, ValueError) as exception:
        raise UnpackException(exception)


def is_ofbac_bad_out_port(code):
    """Check if the code is a OFPBAC_BAD_OUT_PORT error."""
    errors = (v0x01.asynchronous.error_msg.BadActionCode.OFPBAC_BAD_OUT_PORT,
              v0x04.asynchronous.error_msg.BadActionCode.OFPBAC_BAD_OUT_PORT)
    return code in errors


def get_port_config_for_version(version):
    """Return port_config object to a specific version of python-openflow."""
    port_config = None

    if version == 0x01:
        port_config = v0x01.common.phy_port.PortConfig.OFPPC_NO_FWD
    elif version == 0x04:
        port_config = v0x04.common.port.PortConfig.OFPPC_NO_FWD
    return port_config
