"""Automate struct tests."""
import unittest

from pyof.utils import unpack
from tests.raw_dump import RawDump


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

            class MyTest(TestDump):
                @classmethod
                def setUpClass(cls):
                    super().setUpClass()
                    super().set_raw_dump_file('v0x01', 'ofpt_barrier_reply')
                    # Create BarrierReply(xid=5) when needed
                    super().set_raw_dump_object(BarrierReply, xid=5)
                    # As in spec: ``OFP_ASSERT(sizeof(struct ...) == ...);``
                    super().set_minimum_size(8)

        To only test the minimum size and skip packing/unpacking:

        .. code-block:: python3
            class MyTest(TestDump):
                @classmethod
                def setUpClass(cls):
                    super().set_minimum_size(8, BarrierReply)
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

    _new_raw_dump = None
    _new_raw_object = None
    _msg_cls = None
    _min_size = None

    @classmethod
    def set_raw_dump_file(cls, version, basename):
        """Set which raw dump the tests will use.

        Args:
            protocol_version (str): OpenFlow protocol version,
                e.g. ``v0x01``.
            basename (str): The raw filename without extension.
                E.g. ``ofpt_echo_reply``.
        """
        cls._new_raw_dump = lambda: RawDump(version, basename)

    @classmethod
    def get_raw_dump(cls):
        """Return a new instance of :class:`.RawDump`.

        Use the parameters set in :meth:`set_raw_dump_file`.

        Returns:
            RawDump: with parameters previously set using
                :meth:`set_raw_dump_file`.
        """
        if cls._new_raw_dump is None:
            raise FileNotFoundError()
        return cls._new_raw_dump()

    @classmethod
    def set_raw_dump_object(cls, msg_cls, *args, **kwargs):
        """Set how to create the object that is dumped in a raw file.

        Args:
            msg_class (:obj:`type`): The message class that is packed as a
                raw file, followed by its parameters to instantiate an
                object.

        Example:
            ``super().__init__(BarrierReply, xid=5)`` will create
            ``BarrierReply(xid=5)``.
        """
        TestStruct._msg_cls = msg_cls
        cls._new_raw_object = lambda: msg_cls(*args, **kwargs)

    @classmethod
    def get_raw_object(cls):
        """Create a new object of the dumped message.

        Use the class and parameters set in :meth:`set_raw_dump_object`.

        Returns:
            A new object using class and parameters priviously set through
                :meth:`set_raw_dump_object`.
        """
        return cls._new_raw_object()

    @classmethod
    def set_minimum_size(cls, size, msg_cls=None):
        """Set the struct minimum size.

        The minimum size can be found in OF spec. For example,
        :class:`.PhyPort` minimum size is 48 because of
        ``OFP_ASSERT(sizeof(struct ofp_phy_port) == 48);`` (spec 1.0.0).

        Args:
            size (int): The minimum size of the struct, in bytes.
            msg_cls (class): The class (or function) to have its size checked.
                If None, use the same class set in :meth:`set_raw_dump_object`.
        """
        cls._min_size = size
        if msg_cls is not None:
            TestStruct._msg_cls = msg_cls

    def test_pack(self):
        """Check whether packed objects equals to dump file."""
        try:
            raw_file = self.get_raw_dump().read()
            msg = self.get_raw_object()
            packed_obj = msg.pack()
            self.assertEqual(packed_obj, raw_file)
        except FileNotFoundError:
            raise self.skipTest('No raw dump file found.')

    def test_unpack(self):
        """Check whether the unpacked dump equals to expected object."""
        try:
            unpacked = self.get_raw_dump().unpack()
            obj = self.get_raw_object()
            self.assertEqual(unpacked, obj)
        except FileNotFoundError:
            raise self.skipTest('No raw dump file found.')

    def test_minimum_size(self):
        """Test struct minimum size."""
        if self._min_size is None:
            raise self.skipTest('minimum size was not set.')
        obj = TestStruct._msg_cls()
        self.assertEqual(obj.get_size(), self._min_size)

    def test_raw_dump_size(self):
        """Check whether the unpacked dump has the expected size."""
        try:
            unpacked = self.get_raw_dump().unpack()
            obj = self.get_raw_object()
            self.assertEqual(obj.get_size(), unpacked.get_size())
        except FileNotFoundError:
            raise self.skipTest('No raw dump file found.')


class TestStructDump(unittest.TestCase):
    """Run message pack, unpack and get_size tests using bytes struct dump.

    Test the lib with raw dumps. We assume the raw files are valid according
    to the OF specs to check whether our pack, unpack and get_size
    implementations are correct.

    Also, check the minimum size of the struct by instantiating an object with
    no parameters.

    To run the tests, just extends this class and set the 'dump' and 'obj'
    attributes. You can also optionally set the 'min_size' attribute.

    Example:
        .. code-block:: python3

            class TestMatch(TestStructDump):
                dump = b'' # needs to be filled
                obj = pyof.v0x01.common.flow_match.Match(xid=0)
                min_size = 8
    """

    dump = b''
    obj = None
    min_size = 0

    def __init__(self, *args, **kwargs):
        """Constructor to avoid this base class being executed as a test."""
        if self.__class__ == TestStructDump:
            self.run = self.run = lambda self, *args, **kwargs: None
        super().__init__(*args, **kwargs)

    def setUp(self):
        """Setup the instance before testing."""
        self._msg_cls = type(self.obj)
        self._unpacked_dump = self._unpack_dump()
        super().setUp()

    def _unpack_dump(self):
        obj = self._msg_cls()
        obj.unpack(self.dump)
        return obj

    def test_pack(self):
        """Check whether packed objects equals to dump file."""
        self.assertEqual(self.dump, self.obj.pack())

    def test_unpack(self):
        """Check whether the unpacked dump equals to expected object."""
        self.assertEqual(self._unpacked_dump, self.obj)

    def test_get_size(self):
        """Check if get_size method return the correct size."""
        self.assertEqual(self.obj.get_size(), len(self.dump))

    def test_minimum_size(self):
        """Test struct minimum size."""
        if not self.min_size:
            raise self.skipTest('skipped, no minimum size set.')
        obj = self._msg_cls()
        self.assertEqual(obj.get_size(), self.min_size)

    def test_raw_dump_size(self):
        """Check whether the unpacked dump has the expected size."""
        self.assertEqual(self.obj.get_size(), self._unpacked_dump.get_size())


class TestMsgDump(TestStructDump):
    r"""Run message pack, unpack and get_size tests using bytes message dump.

    Test the lib with raw dumps. We assume the raw files are valid according
    to the OF specs to check whether our pack, unpack and get_size
    implementations are correct.

    Also, check the minimum size of the struct by instantiating an object with
    no parameters.

    To run the tests, just extends this class and set the 'dump' and 'obj'
    attributes. You can also optionally set the 'min_size' attribute.

    Example:
        .. code-block:: python3

            class TestHello(TestMsgDump):
                dump = b'\x01\x00\x00\x08\x00\x00\x00\x00'
                obj = pyof.v0x01.symmetric.hello.Hello(xid=0)
                min_size = 8
    """

    def __init__(self, *args, **kwargs):
        """Constructor to avoid this base class beeing executed as a test."""
        if self.__class__ == TestMsgDump:
            self.run = self.run = lambda self, *args, **kwargs: None
        super().__init__(*args, **kwargs)

    def _unpack_dump(self):
        return unpack(self.dump)


class TestMsgDumpFile(TestMsgDump):
    """Run message pack, unpack and get_size tests using message in a dumpfile.

    Test the lib with raw dumps. We assume the raw files are valid according
    to the OF specs to check whether our pack, unpack and get_size
    implementations are correct.

    Also, check the minimum size of the message by instantiating an object with
    no parameters.

    To run the tests, just extends this class and set the 'dumpfile' and 'obj'
    attributes. You can also optionally set the 'min_size' attribute.

    Example:
        .. code-block:: python3

            class TestHelloFileDump(TestMsgDumpFile):
                dumpfile = 'v0x01/ofpt_hello.dat'
                obj = pyof.v0x01.symmetric.hello.Hello(xid=1)

    """

    dumpfile = None

    def __init__(self, *args, **kwargs):
        """Constructor to avoid this base class beeing executed as a test."""
        if self.__class__ == TestMsgDumpFile:
            self.run = self.run = lambda self, *args, **kwargs: None
        super().__init__(*args, **kwargs)

    def setUp(self):
        """Setup the instance before testing."""
        self._read_dump_file()
        super().setUp()

    def _read_dump_file(self):
        dumpfile = f'raw/{self.dumpfile}'
        try:
            with open(dumpfile, 'rb') as fd:
                self.dump = fd.read()
        except FileNotFoundError:
            raise self.skipTest(f'No raw dump file found: {dumpfile}')
