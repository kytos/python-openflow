#!/usr/bin/envpython

from ofp.v0x01.structs import OFPHeader

# Without values
header = OFPHeader()

header.parse('\x07\x20\x00\x00\x00\x00\x00\x00')
print header.version
print header.type
print header.length
print header.xid

# With values
header = OFPHeader(version=7, type=32, length=0, xid=0)
print header.version
print header.type
print header.length
print header.xid
