# Kytos - python-openflow

[![Openflow][of-icon][of-url]
[![Tag][tag-icon]][tag-url]
[![Release][release-icon]][release-url]
[![License][license-icon]][license-url]

[of-icon]: https://img.shields.io/badge/Openflow-1.0.0-brightgreen.svg
[of-url]: https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.0.0.pdf
[tag-icon]: https://img.shields.io/github/tag/kytos/python-openflow.svg
[tag-url]: https://github.com/kytos/python-openflow/tags
[release-icon]: https://img.shields.io/github/release/kytos/python-openvpn.svg
[release-url]: https://github.com/kytos/python-openflow/releases
[license-icon]: https://img.shields.io/github/license/kytos/python-openflow.svg
[license-url]: https://github.com/kytos/python-openflow/blob/master/LICENSE

This is a subproject of the *Kytos* project. This is the library component, in
charge of parsing OpenFlow messages to/from OpenFlow switches.

This library was developed to be used with our main controller, but feel free to
use this code in your projects/controller. Is a very simple and intuitive
library that also can be used to create your own controller.

## python-openflow structure

This project is packed as a python package (`python-openflow`), and contains the
following directory structure:

  - **python-openflow**: contains all the implemented versions of
    the OpenFlow Protocol Parser. Each version is under its own folder
    - Each version is inside its own directory
    - Each version is [incrementally build](#incremental-code) based
      on the previous version
    - Each version has its own unittest suit on the *tests* directory
  - **raw**: raw (binary) OpenFlow Messages, dumped with
    [tcpdump](http://www.tcpdump.org/tcpdump_man.html) used for Tests purposes

### Incremental code

To avoid code repetition this project utilizes an incremental architechture.

This means that the firt version (1.0.0 = v0x01) was fully coded from the
OpenFlow 1.0.0 Protocol. The 1.1 version (v0x02) imports the 1.0 version and
then do the necessary changes to make it compatible with the OpenFlow 1.1.0
Protocol, and the next version follows the same logic.

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
