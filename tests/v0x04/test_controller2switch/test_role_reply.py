"""RoleReply message tests."""
from pyof.v0x04.controller2switch.role_reply import RoleReply
from tests.test_struct import TestStruct


class TestRoleReply(TestStruct):
    """Test the RoleReply message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_role_reply')
        super().set_raw_dump_object(RoleReply, xid=3, role=0,
                                    generation_id=0)
        super().set_minimum_size(24)
