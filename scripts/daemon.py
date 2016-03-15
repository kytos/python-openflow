#!/usr/bin/env python

import SocketServer

from ofp.v0x02.messages import OFPHeader
from ofp.v0x02.enums import OFPType


class TCPSocketHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our controller.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        header_size = 8
        # self.request is the TCP socket connected to the client
        raw_header = self.request.recv(header_size)
        if raw_header:
            #TODO: Should we instanciate with the raw_header ?
            header = OFPHeader()
            header.pack(raw_header)

            raw_message = self.request.recv(header.length.value - header_size)

            #TODO: Create thread to handle header + raw_message

    def show_header(self, header):
            self.debug("Version %d" % header.version.value)
            self.debug("Type: %s" % OFPType().get_name(header.type.value))
            self.debug("Length: %d" % header.length.value)
            self.debug("xid: %d" % header.xid.value)

    def debug(self, msg):
        print("DEBUG: %s", msg)

if __name__ == "__main__":
    HOST, PORT = "localhost", 6633

    # Create the server, binding to localhost on port 6633
    server = SocketServer.TCPServer((HOST, PORT), TCPSocketHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
