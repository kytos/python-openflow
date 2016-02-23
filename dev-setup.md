# Development Setup

This setup tutorial uses Mininet. In order to install Mininet in Linux, please, follow this [link](http://mininet.org/download/)

## Topology Startup

After installing Mininet, create a simple topology with an OpenFlow switch and point the controller to your localhost.

```
# mn --controller=remote,ip='127.0.0.1',listenport=6633
```

## Running the Parser

You can use the example.py available in this repository as a reference to use the OpenFlow parser. To run the example.py follow the instructions bellow.

* Inform the IP address to Listen. 

HOST = IP_Address

* Inform the port number to Listen.

PORT = Port_number

* Set the python path as follow:
```
# export PYTHONPATH=.:$PYTHONPATH
```

* Run the example.py:
```
# python example.py
```
