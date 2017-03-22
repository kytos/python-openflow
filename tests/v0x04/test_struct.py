"""Automate struct tests."""
import unittest

from pyof.v0x04.common.header import Header
from pyof.v0x04.common.utils import new_message_from_header


class TestStruct(unittest.TestCase):
    """Run tests related to struct packing and unpacking.

    Test the lib with raw dump files from an OpenFlow switch. We assume the
    raw files are valid according to the OF specs to check whether our pack and
    unpack implementations are correct.

    Also, check the minimum size of the struct by instantiating an object with
    no parameters.

    To run these tests, just extends this class and call 2 methods in the
    ``setUp`` method like the example.

    Example:
        .. code-block:: python3

            class MyTest(TestStruct):
                @classmethod
                def setUpClass(cls):
                    super().setUpClass()
                    # Create BarrierReply(xid=5)
                    super().set_message(BarrierReply, xid=5)
                    # As in spec: ``OFP_ASSERT(sizeof(struct ...) == ...);``
                    super().set_minimum_size(8)

        To only test the minimum size and skip packing/unpacking:

        .. code-block:: python3
            class MyTest(TestStruct):
                @classmethod
                def setUpClass(cls):
                    super().set_message(BarrierReply)
                    super().set_minimum_size(8)
    """

    def __init__(self, *args, **kwargs):
        """The constructor will avoid that this class tests are executed.

        The tests in this class are executed through the child, so there's no
        no need for them to be executed once more through the parent.
        """
        super().__init__(*args, **kwargs)
        # Override the run method, so it does nothing instead of running the
        # tests (again).
        if self.__class__ == TestStruct:
            self.run = lambda self, *args, **kwargs: None

    _msg_cls = None
    _msg_params = None
    _min_size = None

    @classmethod
    def set_message(cls, msg_cls, *args, **kwargs):
        """Set how to create the message object.

        Args:
            msg_class (:obj:`type`): The message class followed by its
                parameters to instantiate an object.

        Example:
            ``super().__init__(BarrierReply, xid=5)`` will create
            ``BarrierReply(xid=5)``.
        """
        TestStruct._msg_cls = msg_cls
        cls._msg_params = (args, kwargs)

    @classmethod
    def set_minimum_size(cls, size):
        """Set the struct minimum size (from spec).

        The minimum size can be found in OF spec. For example,
        :class:`.PhyPort` minimum size is 48 because of
        ``OFP_ASSERT(sizeof(struct ofp_phy_port) == 48);`` (spec 1.0.0).

        Args:
            size (int): The minimum size of the struct, in bytes.
        """
        cls._min_size = size

    def test_pack_unpack(self):
        """Pack the message, unpack and check whether they are the same."""
        if self._msg_cls:
            args, kwargs = self._msg_params
            self._test_pack_unpack(*args, **kwargs)

    def _test_pack_unpack(self, *args, **kwargs):
        """Pack the message, unpack and check whether they are the same.

        Call this method multiple times if you want to test more than one
        object.
        """
        obj = self._msg_cls(*args, **kwargs)
        packed = obj.pack()
        header = Header()
        header_size = header.get_size()
        header.unpack(packed[:header_size])
        unpacked = new_message_from_header(header)
        unpacked.unpack(packed[header_size:])

        self.assertEqual(packed, unpacked.pack())

    def test_minimum_size(self):
        """Test struct minimum size."""
        if self._min_size is None:
            raise self.skipTest('minimum size was not set.')
        obj = TestStruct._msg_cls()
        self.assertEqual(obj.get_size(), self._min_size)
