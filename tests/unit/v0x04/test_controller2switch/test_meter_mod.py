"""MeterMod tests."""
from unittest import TestCase

from pyof.v0x04.controller2switch.meter_mod import (
    MeterBandDrop, MeterBandDscpRemark, MeterBandExperimenter, MeterBandHeader,
    MeterMod)


class TestMeterMod(TestCase):
    """MeterMod test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(16, MeterMod().get_size())


class TestMeterBandHeader(TestCase):
    """MeterBandHeader test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(12, MeterBandHeader().get_size())


class TestMeterBandDrop(TestCase):
    """MeterBandDrop test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(16, MeterBandDrop().get_size())


class TestMeterBandDscpRemark(TestCase):
    """MeterBandDscpRemark test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(16, MeterBandDscpRemark().get_size())


class TestMeterBandExperimenter(TestCase):
    """MeterBandExperimenter test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(16, MeterBandExperimenter().get_size())
