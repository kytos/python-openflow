#!/usr/bin/env python3

import threading

from socketserver import ThreadingMixIn, BaseRequestHandler
from socketserver import TCPServer as SSTCPServer

from ofp.v0x02.messages import OFPHeader
from ofp.v0x02.enums import OFPType
from ofp.v0x02.exceptions import OFPException

class OpenFlowHandler(BaseRequestHandler):
    """
    The request handler class for our controller.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        self.debug("Handling client %s:%s" % (self.client_address[0],
                                              self.client_address[1]))

        header_size = 8

        try:
            # self.request is the TCP socket connected to the client
            raw_header = self.request.recv(header_size)
            cur_thread = threading.current_thread()
            if raw_header:
                #TODO: Should we instanciate with the raw_header ?
                header = OFPHeader()
                header.unpack(raw_header)
                raw_message = self.request.recv(header.length.value - header_size)

                #TODO: Create method to handle header + raw_message
                #if header.ofp_type == OFPHELLO
                #    self.handle_hello(header, raw_message)
                #elif

        except OFPException as e:
            self.error("Error handling data from %s:%s" % self.client_address)

    def handle_hello(self, header, raw_message):
        pass

    def show_header(self, header):
        self.debug("Version %d" % header.version.value)
        self.debug("Type: %s" % OFPType().get_name(header.type.value))
        self.debug("Length: %d" % header.length.value)
        self.debug("xid: %d" % header.xid.value)

    def debug(self, msg):
        print("DEBUG: %s" % msg)

    def error(self, msg):
        print("ERROR: %s" % msg)

    def info(self, msg):
        print("INFO: %s" % msg)


class TCPServer(ThreadingMixIn, SSTCPServer):
    #daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 6633

    # Create the server, binding to localhost on port 6633
    server = TCPServer((HOST,PORT), OpenFlowHandler)

    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.start()
    print("Server listing at %s:%s" % (server.server_address[0],
                                       server.server_address[1]))
