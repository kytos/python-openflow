# Development Environment

If you wanna contribute to this project please follow the instructions bellow to
setup a development environment.

For more information about this project, and how to install this library, please
read `README.md`.

For now, we don't have a full controller framework. You should use our socket
handle daemon to redirect real OpenFlow messages to the library methods (for
this you can use mininet if you dont have a real OpenFlow Switch).

Alternatively, you can read from raw binary files. It is up to you.

## Using Mininet

In order to use Mininet, you need also a "stub" controller listening on port 6633.
We provide a very basic one, just for tests. Please run our "fake controller":

```
$ python scripts/daemon.py
```

Now, you can install Mininet on Linux. Please, follow [Mininet
Instructions](http://mininet.org/download/)

After installing Mininet, start your mininet with a simple topology with
OpenFlow 1.1.0. Also make sure that the OpenFlow virtual switches will connect
to our "socket daemon" on proper address and port:

```
$ sudo mn --controller=remote,ip='127.0.0.1',listenport=6633
```

## From raw files

We provide some files with raw packets to be used as input with the parser
library. To use our raw packet files, please take a look inside `raw` directory.

# Contributing

## Github issues

## IRC/Mailinglist
