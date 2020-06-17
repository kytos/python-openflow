"""group_mod tests."""
from unittest import TestCase

from pyof.v0x04.controller2switch.group_mod import GroupMod
from pyof.v0x04.common.action import (
    ActionExperimenter, ActionSetField, ListOfActions)
from pyof.v0x04.common.flow_match import OxmClass, OxmOfbMatchField, OxmTLV
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.controller2switch.common import Bucket
from pyof.v0x04.controller2switch.group_mod import  ListOfBuckets


class TestGroupMod(TestCase):
    """group_mod tests."""

    def test_min_size(self):
        """Test minimum struct size."""
        self.assertEqual(16, GroupMod().get_size())


class TestBucket(TestCase):
    """bucket tests."""

    def test_min_size(self):
        """Test minimum struct size."""
        self.assertEqual(16, Bucket().get_size())


class TestListBuckets(TestCase):

    def setUp(self):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUp()

        self.oxmtlv1 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                         oxm_field=OxmOfbMatchField.OFPXMT_OFB_METADATA,
                         oxm_hasmask=False,
                         oxm_value=b'\x00\x00\x00\x00\x00\x00\x00\x01')
        self.oxmtlv2 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                         oxm_field=OxmOfbMatchField.OFPXMT_OFB_METADATA,
                         oxm_hasmask=False,
                         oxm_value=b'\x00\x00\x00\x00\x00\x00\x00\x02')

        self.action1 = ActionSetField(field=self.oxmtlv1)
        self.action2 = ActionSetField(field=self.oxmtlv2)
        self.action3 = ActionExperimenter(length=16, experimenter=0x00002320,
                                     body=b'\x00\x0e\xff\xf8\x28\x00\x00\x00')
        self.action4 = ActionExperimenter(length=16, experimenter=0x00001223,
                                     body=b'\x00\x0e\xff\xff\x28\x00\x00\x00')

    def test_bucket_list(self):

        bucket1 = Bucket(length=48, weight=1, watch_port=PortNo.OFPP_ANY,
                         watch_group=PortNo.OFPP_ANY,
                         actions=ListOfActions([self.action1, self.action2]))
        bucket2 = Bucket(length=80, weight=2, watch_port=PortNo.OFPP_ANY,
                         watch_group=PortNo.OFPP_ANY,
                         actions=ListOfActions([self.action1, self.action2,
                                                self.action3, self.action4]))
        bucket3 = Bucket(length=48, weight=3, watch_port=PortNo.OFPP_ANY,
                         watch_group=PortNo.OFPP_ANY,
                         actions=ListOfActions([self.action3, self.action4]))

        # Packing buckets
        buckets = ListOfBuckets([bucket1, bucket2, bucket3])
        buff = packed_buff = buckets.pack()

        # Unpacking buckets bytes
        unpacked_buckets = ListOfBuckets()
        unpacked_buckets.unpack(buff)

        self.assertEqual(len(unpacked_buckets), 3)
        self.assertEqual(unpacked_buckets[0].length, 48)
        self.assertEqual(unpacked_buckets[0].weight, 1)
        self.assertEqual(len(unpacked_buckets[0].actions), 2)
        self.assertEqual(unpacked_buckets[0].actions[0].field.oxm_value,
                         self.oxmtlv1.oxm_value)
        self.assertEqual(unpacked_buckets[0].actions[1].field.oxm_value,
                         self.oxmtlv2.oxm_value)

        self.assertEqual(unpacked_buckets[1].length, 80)
        self.assertEqual(unpacked_buckets[1].weight, 2)
        self.assertEqual(len(unpacked_buckets[1].actions), 4)
        self.assertEqual(unpacked_buckets[1].actions[0].field.oxm_value,
                         self.oxmtlv1.oxm_value)
        self.assertEqual(unpacked_buckets[1].actions[1].field.oxm_value,
                         self.oxmtlv2.oxm_value)
        self.assertEqual(unpacked_buckets[1].actions[2].body,
                         self.action3.body)
        self.assertEqual(unpacked_buckets[1].actions[3].body,
                         self.action4.body)

        self.assertEqual(unpacked_buckets[2].length, 48)
        self.assertEqual(unpacked_buckets[2].weight, 3)
        self.assertEqual(len(unpacked_buckets[2].actions), 2)
        self.assertEqual(unpacked_buckets[2].actions[0].body,
                         self.action3.body)
        self.assertEqual(unpacked_buckets[2].actions[1].body,
                         self.action4.body)

    def test_buckets_one_item(self):

        bucket1 = Bucket(length=48, weight=1, watch_port=PortNo.OFPP_ANY,
                         watch_group=PortNo.OFPP_ANY,
                         actions=ListOfActions([self.action1, self.action2]))

        # Packing buckets
        buckets = ListOfBuckets([bucket1])
        buff = packed_buff = buckets.pack()

        # Unpacking buckets bytes
        unpacked_buckets = ListOfBuckets()
        unpacked_buckets.unpack(buff)

        self.assertEqual(len(unpacked_buckets), 1)
        self.assertEqual(unpacked_buckets[0].length, 48)
        self.assertEqual(unpacked_buckets[0].weight, 1)
        self.assertEqual(len(unpacked_buckets[0].actions), 2)
        self.assertEqual(unpacked_buckets[0].actions[0].field.oxm_value,
                         self.oxmtlv1.oxm_value)
        self.assertEqual(unpacked_buckets[0].actions[1].field.oxm_value,
                         self.oxmtlv2.oxm_value)

    def test_buckets_no_action(self):

        bucket1 = Bucket(length=48, weight=1, watch_port=PortNo.OFPP_ANY,
                         watch_group=PortNo.OFPP_ANY,
                         actions=ListOfActions([self.action1]))

        # Packing buckets
        buckets = ListOfBuckets([bucket1])
        buff = packed_buff = buckets.pack()

        # Unpacking buckets bytes
        unpacked_buckets = ListOfBuckets()
        unpacked_buckets.unpack(buff)

        self.assertEqual(len(unpacked_buckets), 1)
        self.assertEqual(unpacked_buckets[0].length, 48)
        self.assertEqual(unpacked_buckets[0].weight, 1)
        self.assertEqual(len(unpacked_buckets[0].actions), 1)
        self.assertEqual(unpacked_buckets[0].actions[0].field.oxm_value,
                         self.oxmtlv1.oxm_value)
