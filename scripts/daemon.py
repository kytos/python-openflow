#!/usr/bin/env python

import SocketServer

from ofp.v0x02.messages import *
from ofp.v0x02.enums import OFPType


class OpenFlowHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our controller.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        raw_header = self.request.recv(8)
        if raw_header:
            self.header = OFPHeader()
            self.header.parse(raw_header)
            self.show_header()
        if OFPType().get_name(self.header.type.value) == OFPType.OFPT_HELLO:
            hello = OFPHELLO(xid = self.header.xid.value)
            self.request.sendall(hello.build())

#            if header.type.value == OFPType.OFPT_HELLO:
#                hello = OFPHELLO(xid = header.xid.value)
#                conn.send(hello.build())
#            elif header.type.value == OFPType.OFPT_ECHO_REQUEST:
#                echo = OFPECHOReply()
#                conn.send(echo.build())



    def show_header(self):
            self.debug("Version %d" % self.header.version.value)
            self.debug("Type: %s" % OFPType().get_name(self.header.type.value))
            self.debug("Length: %d" % self.header.length.value)
            self.debug("xid: %d" % self.header.xid.value)
            if self.header.length.value > 8:
                pad = self.request.recv(self.header.length.value - 8)

    def debug(self, msg):
        print "DEBUG: %s" % msg
           
if __name__ == "__main__":
    HOST, PORT = "localhost", 6633

    # Create the server, binding to localhost on port 6633
    server = SocketServer.TCPServer((HOST, PORT), OpenFlowHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
