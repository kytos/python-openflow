# Problem Statement

The file openFlow.pcap available in this repository contains raw packets collected from a OpenFlow switch (first 50 packets exchanged with the controller). Your task is, parse the raw packets in this file and print the maximum information you can gather from the OpenFlow packets. 
In this file you will find a HELLO packet and a FEATURES_REPLY packet.

Please refer to the [OpenFlow 1.1 specification](http://archive.openflow.org/documents/openflow-spec-v1.1.0.pdf) on page 24 (specs about open flow headers), page 55 (specs about HELLO messages) and page 36 (specs about FEATURES_REPLY messages).
