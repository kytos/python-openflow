#!/usr/bin/env python

import socketserver
import threading

from ofp.v0x02.messages import OFPHeader
from ofp.v0x02.enums import OFPType


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
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
        cur_thread = threading.current_thread()
        print("  Curr Thread: ",cur_thread)
        if raw_header:
            #TODO: Should we instanciate with the raw_header ?
            header = OFPHeader()
            header.unpack(raw_header)
            raw_message = self.request.recv(header.length.value - header_size)
            print("XID: ", header.xid.value)

            #TODO: Create thread to handle header + raw_message

    def show_header(self, header):
            self.debug("Version %d" % header.version.value)
            self.debug("Type: %s" % OFPType().get_name(header.type.value))
            self.debug("Length: %d" % header.length.value)
            self.debug("xid: %d" % header.xid.value)

    def debug(self, msg):
        print("DEBUG: %s", msg)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    HOST, PORT = "localhost", 6633

    # Create the server, binding to localhost on port 6633
    server = ThreadedTCPServer((HOST,PORT),ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    #server = socketserver.TCPServer((HOST, PORT), TCPSocketHandler)
    print("Server loop running in thread:", server_thread.name)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
