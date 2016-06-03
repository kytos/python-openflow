# Kytos - python-openflow

[![Openflow][of-icon]][of-url]
[![Tag][tag-icon]][tag-url]
[![Release][release-icon]][release-url]
[![License][license-icon]][license-url]

*python-openflow* is a low level library to parse OpenFlow messages. If you want
to read an OpenFlow packet from an open socket or send a message to an OpenFlow
switch, this is your best friend.

This library is part of *Kytos* project and was developed to be used with
*Kytos* controller, but feel free to use this simple and intuitive library in
another project with another controller.

For more information about, please visit our [Kytos web site][kytos-url].

## Installing

You can install this package from source or via pip. If you have cloned this
repository and want to install it via `setuptools`, please run:

```shell
sudo python3 setup.py install
```

Or, to install via pip, please execute:

```shell
sudo pip3 install python-openflow
```

## Usage

For example, see how it is easy to create a feature request message with this
library. You can use ipython3 to get the advantages of autocompletion:

```python
>>> from pyof.v0x01.controller2switch.features_request import FeaturesRequest
>>> request = FeaturesRequest(xid = 100)
>>> print(request.header)
<pyof.v0x01.common.header.Header object at 0x7efd33bb2780>
>>> print(request.header.message_type)
Type.OFPT_FEATURES_REQUEST
>>> print(request.header.xid)
100
```

If you need to send this message via socket, call the `pack()` method to get its
binary representation:

```python
>>> binary_msg = request.pack()
```

For a more detailed documentation, please check the [python-openflow API
Reference Manual][api-reference-url].

## Main Highlights

### Speed focused

We keep the word *performance* in mind since the beginning of the development.
Also, as computer scientists, we will always try to get the best performance by
using the most suitable algorithms.

Some of our developers participated in several demonstrations involving tests
with high-speed networks (~1 terabit/s), some even involving data transfers
from/to CERN.

### Always updated

To avoid code repetition this project utilizes an incremental architecture.

This means that the first version (1.0.0 = v0x01) was coded from the full
OpenFlow 1.0.2 Protocol. The 1.1 version (v0x02) imports the 1.0 version and
then do the necessary changes to make it compatible with the OpenFlow 1.1.0
Protocol, and the next version follows the same logic.

Using incremental code makes the implementation of new versions of OpenFlow
protocol faster. Our main goal is to follow the specifications since the very
beginning.

### Easy to learn

Python is an easy language to learn and we aim at writing code in a "pythonic
way". We also provide a well documented API. Thus, learning to make your
controller using this library is a trivial task.

### Born to be free

OpenFlow was born with a simple idea: make your network more vendor agnostic
and we like that!

We are advocates and supporters of free software and we believe that the more
eyes observe the code, the better it will be. This project can receive support
from many vendors, but will never follow a particular vendor direction.

*python-openflow* will always be free software.

## Authors

This is a collaborative project between SPRACE (From São Paulo State University,
Unesp) and Caltech (California Institute of Technology). For a complete list of
authors, please open `AUTHORS.md` file.

## Contributing

If you want to contribute to this project, please read
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
[license-icon]: https://img.shields.io/github/license/kytos/python-openflow.svg
[license-url]: https://github.com/kytos/python-openflow/blob/master/LICENSE
