#!/usr/bin/env python

from ofp.v0x01.messages import *
from ofp.v0x01.enums import OFPType

import socket
import sys

HOST = "localhost"
PORT = 6633

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connected by', addr

msg = OFPFeaturesRequest()
msg_raw = msg.build()

while 1:
    try:
        pad = None
        header_raw = conn.recv(8) # read header
        if header_raw:
            header = OFPHeader()
            header.parse(header_raw)
            print "Version %d" % header.version.value
            print "Type: %s" % OFPType().get_name(header.type.value)
            print "Length: %d" % header.length.value
            print "xid: %d" % header.xid.value
            if header.length.value > 8:
                pad = conn.recv(header.length.value - 8)

            if header.type.value == OFPType.OFPT_HELLO:
                hello = OFPHELLO(xid = header.xid.value)
                conn.send(hello.build())
            elif header.type.value == OFPType.OFPT_ECHO_REQUEST:
                echo = OFPECHOReply()
                conn.send(echo.build())
    except:
        conn.close()

conn.close()
