# Development Environment

If you wanna contribute to this project please follow the instructions bellow to
setup a development environment.

For more information about this project, please read `README.md`.

For now, we don't have a full controller framework. You should use our socket
handle daemon to redirect real OpenFlow messages to the library methods (for
this you can use mininet if you dont have a real OpenFlow Switch).

Alternatively, you can read from raw binary files. It is up to you.

## Using Mininet


In order to install Mininet on Linux, please, follow [Mininet
Instructions](http://mininet.org/download/)

After installing Mininet, start your mininet with a simple topology with
OpenFlow 1.1.0. Also make sure that the OpenFlow virtual switches will connect
to our "socket daemon" on proper address and port:

```
# mn --controller=remote,ip='127.0.0.1',listenport=6633
```

## From raw files

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
