# Kytos - python-openflow

[![Openflow][of-icon]][of-url]
[![Tag][tag-icon]][tag-url]
[![Release][release-icon]][release-url]
[![Tests][tests-icon]][tests-url]
[![License][license-icon]][license-url]

*python-openflow* is a low level library to parse OpenFlow messages. So if you
open a socket and wanna read an OpenFlow packet, or wanna send a message to an
OpenFlow switch, this is your best friend.

This library is part of *Kytos* project and was developed to be used with
*Kytos* controller, but feel free to use this library in your
project/controller. Is a very intuitive and simple library.

For more information about, please visit our [Kytos web site][kytos-url].

## Installing

You can install this package from sources or via pip. If you have cloned this
repository and wanna install via `setuptools`, please run:

  ```shell
  sudo python3 setup.py install
  ```

Or, if you wanna install via pip, please execute:

  ```shell
  sudo pip3 install python-openflow
  ```

## Usage

Look, how it is easy to create a feature request message with this library. You
can use ipython3 to get advantages of auto complete:

  ```python
  >>> from pyof.v0x01.controller2switch.features_request import FeaturesRequest
  >>> request = FeaturesRequest(xid = 100)
  >>> print(request.header)
  <pyof.v0x01.common.header.Header object at 0x7efd33bb2780>
  >>> print(request.header.message_type)
  Type.OFPT_FEATURES_REPLY
  >>> print(request.header.xid)
  100
  ```

If you need to send this message via socket, you can call `pack()` method to get
the binary representation of this object:

  ```python
  >>> data = request.pack()
  ```

For a more detailed documentation, please visit [python-openflow API Reference
Manual][api-reference-url].

## Main Highlights

### Speed focused

We keep the word performance in mind since the beginning of the development.
Also, as computer scientists we will always try to get the best performance by
using the most suitable algorithm.

Some developers participated in several demonstrations involving tests with
high-speed networks (~ 1 terabit/s), some even involving data transfers from/to
CERN.

### Always updated

To avoid code repetition this project utilizes an incremental architecture.

This means that the first version (1.0.0 = v0x01) was fully coded from the
OpenFlow 1.0.0 Protocol. The 1.1 version (v0x02) imports the 1.0 version and
then do the necessary changes to make it compatible with the OpenFlow 1.1.0
Protocol, and the next version follows the same logic.

Using incremental code makes the implementation of new versions of OpenFlow
protocol faster. Yes, we are at initial stages of development, but our main goal
is always follow the specs.

### Easy to learn

We try to code in a "pythonic way" always. We also have a well documented API.
Learn to make your controller using this library is a trivial task.

### Born to be free

OpenFlow was born with a simple idea: make your network more vendor agnostic
and we like that!

We are advocates and supporters of free software and we believe that the more
eyes observe a certain code, a better code will be generated. This project can
receive support of many vendors, but never will follow a particular vendor
direction.

We always will keep this code open.

## Authors

This is a collaborative project between SPRACE (From São Paulo State University,
Unesp) and Caltech (California Institute of Technology). For a complete list of
authors, please open `AUTHORS.md` file.

## Contributing

If you wanna contribute with this project, please read
[CONTRIBUTE.md](CONTRIBUTE.md) and [HACKING.md](HACKING.md) files.

## License

This software is under _MIT-License_. For more information please read `LICENSE`
file.

[api-reference-url]: http://docs.kytos.io/python-openflow/api-reference/
[kytos-url]: http://kytos.io/
[of-icon]: https://img.shields.io/badge/Openflow-1.0.0-brightgreen.svg
[of-url]: https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.0.0.pdf
[tag-icon]: https://img.shields.io/github/tag/kytos/python-openflow.svg
[tag-url]: https://github.com/kytos/python-openflow/tags
[release-icon]: https://img.shields.io/github/release/kytos/python-openvpn.svg
[release-url]: https://github.com/kytos/python-openflow/releases
[tests-icon]: https://kytos.io/imgs/tests-status.svg
[tests-url]: https://github.com/kytos/python-openflow
[license-icon]: https://img.shields.io/github/license/kytos/python-openflow.svg
[license-url]: https://github.com/kytos/python-openflow/blob/master/LICENSE
