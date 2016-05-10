# Kytos - python-openflow

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

## OpenFlow Protocol Specification Implemented Versions

 - [OpenFlow 1.0.0 Protocol](https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.0.0.pdf)

More versions and other technical documents at: https://www.opennetworking.org/sdn-resources/technical-library

## Contributing

If you wanna contribute with this project, please read
[CONTRIBUTE.md](CONTRIBUTE.md) and [HACKING.md](HACKING.md) files.
