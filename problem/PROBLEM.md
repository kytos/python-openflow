# Problem Statement

The OpenFlow is a network protocol to comunicate with Network Switches. Is a
traditional client/server model protocol.

The file `ofpt_hello.dat` available in this repository contain one raw packet
collected from tcpdump. And this packet has a message from an OpenFlow switch
(server) to our OpenFlow controller (client).

Your task is parse this raw packet using the OpenFlow v.1.1.0 specification.
You must print on stdout the maximum amount of information that you can.

This is a binary file  with only one message: a `OFPT_HELLO` packet.

You can use Google or any another resource to finish this task, also please
refer to the [OpenFlow 1.1.0 Specification](http://goo.gl/yjlGX2)

 - Page 24: Specs about open flow headers;
 - Page 55: Specs about `OFPT_HELLO` messages.
