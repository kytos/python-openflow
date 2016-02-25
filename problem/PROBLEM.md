# Problem Statement

The OpenFlow is a network protocol used to define how the communication between 
Network Switches and hosts will happen. This protocol is implemented using a 
traditional client/server architecture.

The file `ofpt_hello.dat` available in this repository contain one raw packet
collected from tcpdump. This packet contains a message from an OpenFlow switch
(server) to our OpenFlow controller (client).

Your task is to write a parser for this raw packet using the OpenFlow v.1.0 
specification. You must print on stdout the maximum amount of information that 
you can.

This is a binary file with only one message: a `OFPT_HELLO` packet.

You can use Google or any another resource to finish this task, also please
refer to the [OpenFlow 1.0 Specification](http://goo.gl/M9W1h3)

 - Page 2: Specs about open flow headers;
 - Page 41: Specs about `OFPT_HELLO` messages.