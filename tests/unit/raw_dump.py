"""Help reading raw dump files."""
from pyof.v0x01.common.header import Header
from pyof.v0x01.common.utils import new_message_from_header


class RawDump:
    """A helper to deal with paths and reading raw files.

    Attributes:
        content (bytes): Raw file's content.
    """

    _HEADER_BYTES = 8  # According to OF Protocol specification

    def __init__(self, version, basename):
        """Information to locate the dump file.

        Args:
            version (str): OpenFlow protocol version, e.g. ``v0x01``.
            basename (str): Only the filename without extension.
                E.g. ``ofpt_echo_reply``.
        """
        self._path = 'raw/{}/{}.dat'.format(version, basename)

    def __repr__(self):
        return repr(self.unpack())

    def __bytes__(self):
        return self.read()

    def read(self):
        """Read the raw file.

        Returns:
            bytes: Raw file's content.
        """
        with open(self._path, 'rb') as file:
            return file.read()

    def unpack(self):
        """Unpack header and message from a byte sequence.

        Returns:
            The object type specified in the header with the corresponding
            header.
        """
        content = self.read()
        raw_header = content[:self._HEADER_BYTES]
        header = _unpack_header(raw_header)
        raw_msg = content[self._HEADER_BYTES:header.length.value]
        return _unpack_message(header, raw_msg)


def _unpack_header(raw_header):
    header = Header()
    header.unpack(raw_header)
    return header


def _unpack_message(header, raw_msg):
    msg = new_message_from_header(header)
    msg.unpack(raw_msg)
    return msg
