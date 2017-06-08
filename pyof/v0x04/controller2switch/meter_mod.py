"""Meter modification message."""
from enum import IntEnum

from pyof.foundation.base import GenericBitMask, GenericMessage
from pyof.foundation.basic_types import (
    FixedTypeList, GenericStruct, Pad, UBInt8, UBInt16, UBInt32)
from pyof.v0x04.common.header import Header, Type

__all__ = ('MeterMod', 'Meter', 'MeterModCommand', 'MeterFlags',
           'MeterBandHeader', 'MeterBandType', 'MeterBandDrop',
           'MeterBandDscpRemark', 'MeterBandExperimenter')


class Meter(IntEnum):
    """Meter numbering. Flow meters can use any number up to OFPM_MAX."""

    #: Last usable meter.
    OFPM_MAX = 0xffff0000

    # Virtual meters.
    #: Meter for slow datapath, if any.
    OFPM_SLOWPATH = 0xfffffffd
    #: Meter for controller connection.
    OFPM_CONTROLLER = 0xfffffffe
    #: Represents all meters for stat requests commands.
    OFPM_ALL = 0xffffffff


class MeterModCommand(IntEnum):
    """Meter commands."""

    #: New meter.
    OFPMC_ADD = 0
    #: Modify specified meter.
    OFPMC_MODIFY = 1
    #: Delete specified meter.
    OFPMC_DELETE = 2


class MeterFlags(GenericBitMask):
    """Meter configuration flags."""

    #: Rate value in kb/s (kilo-bit per second).
    OFPMF_KBPS = 1 << 0
    #: Rate value in packet/sec.
    OFPMF_PKTPS = 1 << 1
    #: Do burst size.
    OFPMF_BURST = 1 << 2
    #: Collect statistics.
    OFPMF_STATS = 1 << 3


class MeterBandType(IntEnum):
    """Meter band types."""

    #: Drop packet.
    OFPMBT_DROP = 1
    #: Remark DSCP in the IP header.
    OFPMBT_DSCP_REMARK = 2
    #: Experimenter meter band.
    OFPMBT_EXPERIMENTER = 0xFFFF

    def find_class(self):
        """Method used to return a class related with this type."""
        types = {1: MeterBandDrop, 2: MeterBandDscpRemark,
                 3: MeterBandExperimenter}
        return types[self.value]


class MeterBandHeader(GenericStruct):
    """Common header for all meter bands."""

    band_type = UBInt16(enum_ref=MeterBandType)
    length = UBInt16()
    rate = UBInt32()
    burst_size = UBInt32()

    def __init__(self, band_type=None, rate=None, burst_size=None):
        """Instance attributes assignments.

        Args:
            band_type (MeterBandType): One of OFPMBT_*.
            rate (int): Rate for this band.
            burst_size (int): Size of bursts.
        """
        super().__init__()
        self.band_type = band_type
        self.rate = rate
        self.burst_size = burst_size
        self.update_length()

    def update_length(self):
        """Update the length attribute of current instance."""
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
        band_type = UBInt16(enum_ref=MeterBandType)
        band_type.unpack(buff, offset)
        self.__class__ = MeterBandType(band_type.value).find_class()

        length = UBInt16()
        length.unpack(buff, offset=offset+2)

        super().unpack(buff[:offset+length.value], offset)


class MeterMod(GenericMessage):
    """Meter configuration."""

    header = Header(message_type=Type.OFPT_METER_MOD)
    command = UBInt16(enum_ref=MeterModCommand)
    flags = UBInt16(enum_ref=MeterFlags)
    meter_id = UBInt32()
    bands = FixedTypeList(MeterBandHeader)

    def __init__(self, xid=None, command=None, flags=None, meter_id=None,
                 bands=None):
        """Instance attributes assignment.

        Args:
            xid (int): Headers transaction id. Defaults to random.
            command (MeterModCommand): One of OFPMC_*.
            flags (MeterFlags): One of OFPMF_*.
            meter_id (int): Meter instance.
            bands (MeterBandHeader): The bands length is inferred from the
                length field in the header.
        """
        super().__init__(xid)
        self.command = command
        self.flags = flags
        self.meter_id = meter_id
        self.bands = bands


class MeterBandDrop(MeterBandHeader):
    """OFPMBT_DROP band - drop packets."""

    pad = Pad(4)

    def __init__(self, rate=None, burst_size=None):
        """Instance attributes assignment.

        Args:
            rate (int): Rate for dropping packets.
            burst_size (int): Size of bursts.
        """
        super().__init__(MeterBandType.OFPMBT_DROP, rate, burst_size)


class MeterBandDscpRemark(MeterBandHeader):
    """OFPMBT_DSCP_REMARK band - Remark DSCP in the IP header."""

    prec_level = UBInt8()
    pad = Pad(3)

    def __init__(self, rate=None, burst_size=None, prec_level=None):
        """Instance attributes assignment.

        Args:
            rate (int): Rate for remarking packets.
            burst_size (int): Size of bursts.
            prec_level (int): Number of precendence level to substract.
        """
        super().__init__(MeterBandType.OFPMBT_DSCP_REMARK, rate, burst_size)
        self.prec_level = prec_level


class MeterBandExperimenter(MeterBandHeader):
    """OFPMBT_EXPERIMENTER band - Write actions in action set."""

    experimenter = UBInt32()

    def __init__(self, rate=None, burst_size=None, experimenter=None):
        """Instance attributes assignment.

        Args:
            rate (int): Rate for remarking packets.
            burst_size (int): Size of bursts.
            experimenter (int): Experimenter ID which takes the same form as in
                :class:`.ExperimenterHeader`.
        """
        super().__init__(MeterBandType.OFPMBT_EXPERIMENTER, rate, burst_size)
        self.experimenter = experimenter


class ListOfMeterBandHeader(FixedTypeList):
    """List of MeterBandHeader.

    Represented by instances of MeterBandHeader.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
        items (MeterBandHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=MeterBandHeader, items=items)
