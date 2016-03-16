#!/usr/bin/env python

import socketserver

from ofp.v0x02.messages import OFPHeader
from ofp.v0x02.enums import OFPType


class TCPSocketHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our controller.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    daemon_threads = True
    allow_reuse_address = True

    def handle(self):
        header_size = 8
        # self.request is the TCP socket connected to the client
        raw_header = self.request.recv(header_size)
        if raw_header:
            #TODO: Should we instanciate with the raw_header ?
            header = OFPHeader()
            header.unpack(raw_header)
            raw_message = self.request.recv(header.length.value - header_size)
            print(header.xid.value)
            print(header.length.value)

            #TODO: Create thread to handle header + raw_message

    def show_header(self, header):
            self.debug("Version %d" % header.version.value)
            self.debug("Type: %s" % OFPType().get_name(header.type.value))
            self.debug("Length: %d" % header.length.value)
            self.debug("xid: %d" % header.xid.value)

    def debug(self, msg):
        print("DEBUG: %s", msg)


class OFPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    HOST, PORT = "localhost", 6633

    # Create the server, binding to localhost on port 6633
    server = OFPServer((HOST,PORT),TCPSocketHandler)
    #server = socketserver.TCPServer((HOST, PORT), TCPSocketHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
