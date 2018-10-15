##########
Change log
##########
All notable changes to the python-openflow project are documented in this file.

UNRELEASED - Under development
******************************
Added
=====

Changed
=======

Deprecated
==========

Removed
=======

Fixed
=====

Security
========

[2018.2b2] - "ernesto" beta2 - 2018-10-15
***************************************
No changes since the last release.

[2018.2b1] - "ernesto" beta1 - 2018-9-6
***************************************
No changes since the last release.

[2018.1b3] - "dalva" beta3 - 2018-6-15
***************************************
Added
=====
- Improve documentation to use kytos sphinx theme

[2018.1b2] - "dalva" beta2 - 2018-4-20
***************************************
No changes since the last release.

[2018.1b1] - "dalva" beta1 - 2018-3-09
***************************************
Added
=====
- [v0x01] added optional elements in Hello class
- [v0x04] added pack/unpack methods for Hello Elements
- Improve Ethernet class to accept a list of VLANs

Changed
=======
- Some class names to singular: MultipartTypes, ConfigFlags, StatusTypes

[2017.2b2] - "chico" beta2 - 2017-12-01
***************************************
Added
=====
- Better debugging: attribute name in PackException message.
- EtherType Enum.
- [v0x04] get_field method on Match class.
- [v0x04] in_port property on PacketIn class.
- [v0x04] instructions field in FlowStats.
- Attribute name to PackException
- Every message sent by the controller now has its own XID.

Changed
=======
- Using EtherType enum items instead of hardcoded values.
- Default values for many v0x04 classes.
- Default values for many v0x01 classes.
- IPAddress class: Added netmask optional attribute on init.

Removed
=======
- Some unused test files.

Fixed
=====
- Performance issues related to deepcopy operations.
- Unpacking performance issues.
- [v0x04] Multipart message name.
- [v0x04] ErrorMessage unpack.
- [v0x04] ActionSetField.
- [v0x04] MultipartReply unpack.
- [v0x04] FlowStats unpack.
- [v0x04] get_size method of Actions.
- Several bug fixes.

[2017.2b1] - "chico" beta1 - 2017-09-19
***************************************
Added
=====
- OpenFlow Extensible Match structures.
- ARP packet pack/unpack support.
- 802.1q VLAN packet pack/unpack support.

Changed
=======
- Improved packet validation and unpacking.
- Yala substitutes Pylama as the main linter checker.
- Requirements files updated and restructured.

Removed
=======
- Unused and duplicated files.

Fixed
=====
- Some missing classes and elements were included.
- Some test fixes.
- Several bug fixes.


[2017.1] - "bethania" - 2017-07-06
**********************************
Changed
=======
- Documentation updated and improved.

Fixed
=====
- Some bug fixes.


[2017.1b3] - "bethania" beta3 - 2017-06-16
******************************************
Added
=====
- IPv4 packet pack/unpack support.

Changed
=======
- Raise ValueError if not using bytes (e.g. string) in BinaryData.
- Changed docs to show a dropdown button with all python-openflow releases.

Fixed
=====
- [v0x01] Fixed method to unpack error messages.
- documentation: fixed links and build warnings.
- A few bug fixes.


[2017.1b2] - "bethania" beta2 - 2017-05-05
******************************************
Added
=====
- Continuous integration, with Code Quality Score and test coverage.

Changed
=======
- Attributes with Python reserved names were renamed:
    - :code:`len` was renamed to :code:`length`
    - :code:`type` and :code:`property` received a prefix with the Class name.
- Enums of the OpenFlow structures changed to IntEnums, to make easier
  comparisons with integer values.
- Updated requirements.txt
- 'data' fields included for symmetric messages, like echo requests/replies.
- Documentation updated.

Removed
=======
- [v0x02] references, as it is not implemented yet.

Fixed
=====
- Pypi package is fixed and working.
- Several bug fixes.


[2017.1b1] - "bethania" beta1 - 2017-03-24
******************************************
Added
=====
- OF v0x04 - 1.3.5 - version support

Changed
=======
- v0x04
    - Finished implementation
    - Test improvements
- v0x01 - Numerous Fixes
- New and updated tests for 0x04
- OF v0x04 1.3.0 - Compliance fixes
- Test improvements
- Refactoring:
    - Use of Python 3.6 class attribute order preservation
    - New inheritance model, MetaStruct refactored
- Support for Python 3.6 and later
- Improved docs organization
- Added support to AggregationStats and FlowStats
- StatsRequest/Reply packing/unpacking
- Updated docs: install instructions
- Test improvements: fixes, refactoring.
- Refactoring: basic_types.py
- [v0x04] Adding multipart reply and request messages with tests
- Numerous 0x04 implementations
- Improved continuous integration
- v0x01 fixes
- Adding constant files to manage constants in NApps
- Moving foundation module to pyof root folder (same with tests)

[2016.2a1] - alpha1 - 2016-09-11
********************************
Changed
=======
- Enum fixes
- More detailed unpack error messages
- Refactoring: import classes instead of modules
- lint fixes and docs generation
- Pip support

[2016.1a1] - alpha1 - 2016-08-06
********************************
Changed
=======
- many doc and docstrings fixes and enhancements
    - from markdown to restructuredtext
    - doctests
- pypi
- code optimizations.
- many unittests added
- Pack, Unpack and GenericType refactor.
- added GenericBitMask class
- BitMask classes can behave like enums
- python3 compliance on MetaStruct inheritance declaration
- revision of bitmasks and enums
- fixes on enums and GenericStruct inheritance
- object equality comparison on Generic Types and Structs
- Refactor to accept Python basic types as messages attributes.
- Messages type conversion during the pack operation.
- Better documentation
- Several fixes, including GenericMessage pack method.
- Added ConstantTypeList and ListOf* classes
- Added BinaryData into packet in and out
- Added new basic types and new exceptions
- Changed message types from GenericStruct to GenericMessage
- Added FeaturesReply Class
- Validation on pack
- Fix Package setup
- Docs: added support for Sphinx
- new workflow for the project
    - Added explanation and figures to illustrate the workflow.
    - Added a special workflow to hotfix and security fix.
- better readme on contribute and hacking
    - added a test badge to readme
    - update LICENSE
- Numerous test improvements
    - Enable test on setup with setuptools
    - Added some files with OpenFlow binary data for testing
- added Port Status messages class and enums definitions
- added vendor message file and class implementation
- Recode to transform the project into a Python Project
- multiple stats messages implementations
- added requirements file.
- improvements to project structure
- added Project Structure section on README
- pack / unpack refactoring for compliance with OF v0x01
- added unit tests
- docstrings documentation improvements
- Test restructure
- Added MIT License
- several compilation fixes.
- package and imports structure refactoring.
- Added classes for flow statistics.
- Classes to improve Exception Handling
- refactoring to use python3 Enum class
- Added thread implementation for socket handle.
- Use of metaclasses for messages and structs implementation.
- Fixes on HELLO Packet implementation
- initial skeleton to implement introspection
- MessageGeneric class
- better readme and hacking instructions
- better organization on problem description
- added messages, todo and instructions

[2013.1a1] - Initial - 2013-08-06
*********************************
Added
=====
- initial implementation
- support for OF v0x01 messages building and parsing
