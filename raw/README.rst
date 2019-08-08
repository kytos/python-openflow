Generating raw dump files
=========================

OpenFlow 1.0
------------

1. POX - version 0.2.0 (carp), cloned from `GitHub
   <https://github.com/noxrepo/pox.git>`_:

   - ``./pox.py openflow.of_01 --address=127.0.0.1 --port=6633 py``

2. Wireshark - version 2.0.4 with `openflow plugin
   <http://www.projectfloodlight.org/openflow.lua>`_:

   - Choose *loopback* interface;
   - Filter by *of*;
   - Start capturing;
   - After running Mininet as described below, in order to save the OpenFlow content in a dump file,
     right click in the *OpenFlow* tree and then *Export Selected Bytes...*. All done!

3. Mininet - version 2.2.1

   - ``sudo mn --controller=remote,ip='127.0.0.1',listenport=6633 --switch ovs,protocols=OpenFlow10``


OpenFlow 1.3
------------

1. POX forked version, cloned from `GitHub
   <https://github.com/vsulak/pox-1.3.git>`_:

   - ``./pox.py openflow.of_04 --address=127.0.0.1 --port=6653 py``

2. Wireshark - version 2.0.4 with `openflow plugin
   <http://www.projectfloodlight.org/openflow.lua>`_:

   - Choose *loopback* interface;
   - Filter by *of*;
   - Start capturing;
   - After running Mininet as described below, in order to save the OpenFlow content in a dump file,
     right click in the *OpenFlow* tree and then *Export Selected Bytes...*. All done!

3. Mininet - version 2.2.1

   - ``sudo mn --controller=remote,ip='127.0.0.1',listenport=6653 --switch ovs,protocols=OpenFlow13``
