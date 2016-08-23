Generating raw dump files
=========================

1. POX - version 0.2.0 (carp), cloned from `GitHub
   <https://github.com/noxrepo/pox.git>`_:

   a. ``./pox.py openflow.of_01 --address=127.0.0.1 --port=6633 py``

1. Wireshark - version 2.0.4 with `openflow plugin
   <http://www.projectfloodlight.org/openflow.lua>`_:

   a. Choose *loopback* interface;
   a. Filter by *of*;
   a. Start capturing;
   a. After running Mininet as described below, in order to save the OpenFlow
      content in a dump file, right click in the *OpenFlow* tree and then
      *Export Selected Bytes...*. All done!

1. Mininet - version 2.2.1

   a. ``sudo mn --controller=remote,ip='127.0.0.1',listenport=6633 --switch ovs,protocols=OpenFlow10``
