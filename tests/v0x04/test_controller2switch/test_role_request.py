"""RoleRequest message tests."""
from pyof.v0x04.controller2switch.role_request import RoleRequest
from tests.test_struct import TestStruct


class TestRoleRequest(TestStruct):
    """Test the RoleRequest message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_role_request')
        super().set_raw_dump_object(RoleRequest, xid=3, role=0,
                                    generation_id=0)
        super().set_minimum_size(24)
