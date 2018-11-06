"""Base and fundamental classes used all over the library.

Besides classes, several constants are defined here. We designed
python-openflow in a manner to make it easy to create new messages and OpenFlow
structs. You can realize that when you see a message class definition.

A **struct** here is a group of basic attributes and/or struct attributes (i.e.
:class:`~pyof.v0x01.common.header.Header`). A **message** here is like a
struct, but all messages have a header attribute (i.e.
:class:`~pyof.v0x01.asynchronous.packet_in.PacketIn`).


The main classes of this module are :class:`GenericStruct`,
:class:`GenericMessage`, :class:`GenericBitMask` and :class:`GenericType`.
These classes are used in all parts of this library.
"""

# System imports
import importlib
import re
import struct
from collections import OrderedDict
from copy import deepcopy
from enum import Enum, IntEnum
from random import randint

from pyof.foundation.constants import UBINT32_MAX_VALUE as MAXID
from pyof.foundation.exceptions import (
    BadValueException, PackException, UnpackException, ValidationError)

# Third-party imports


# This will determine the order on sphinx documentation.
__all__ = ('GenericStruct', 'GenericMessage', 'GenericType', 'GenericBitMask',
           'MetaStruct', 'MetaBitMask')

# Classes


class GenericType:
    """Foundation class for all custom attributes.

    Base class for :class:`~.UBInt8`, :class:`~.Char`
    and others.
    """

    _fmt = None

    def __init__(self, value=None, enum_ref=None):
        """Create a GenericType with the optional parameters below.

        Args:
            value: The type's value.
            enum_ref (type): If :attr:`value` is from an Enum, specify
                its type.
        """
        self._value = value
        self.enum_ref = enum_ref

    def __deepcopy__(self, memo):
        """Improve deepcopy speed."""
        return type(self)(value=self._value, enum_ref=self.enum_ref)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._value)

    def __str__(self):
        return '{}'.format(str(self._value))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pack() == other.pack()
        elif hasattr(other, 'value'):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return self._value != other

    def __gt__(self, other):
        return self._value > other

    def __ge__(self, other):
        return self._value >= other

    def __lt__(self, other):
        return self._value < other

    def __le__(self, other):
        return self._value <= other

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return self.value - other

    def __or__(self, other):
        return self.value | other

    def __ror__(self, other):
        return self.value | other

    def __and__(self, other):
        return self.value & other

    def __rand__(self, other):
        return self.value & other

    def __xor__(self, other):
        return self.value ^ other

    def __rxor__(self, other):
        return self.value ^ other

    def __lshift__(self, shift):
        return self.value << shift

    def __rshift__(self, shift):
        return self.value >> shift

    def __len__(self):
        return self.get_size()

    @property
    def value(self):
        """Return this type's value.

        Returns:
            object: The value of an enum, bitmask, etc.

        """
        if self.isenum():
            if isinstance(self._value, self.enum_ref):
                return self._value.value
            return self._value
        elif self.is_bitmask():
            return self._value.bitmask
        else:
            return self._value

    def pack(self, value=None):
        r"""Pack the value as a binary representation.

        Considering an example with UBInt8 class, that inherits from
        GenericType:

        >>> from pyof.foundation.basic_types import UBInt8
        >>> objectA = UBInt8(1)
        >>> objectB = 5
        >>> objectA.pack()
        b'\x01'
        >>> objectA.pack(objectB)
        b'\x05'

        Args:
            value: If the value is None, then we will pack the value of the
                current instance. Otherwise, if value is an instance of the
                same type as the current instance, then we call the pack of the
                value object. Otherwise, we will use the current instance pack
                method on the passed value.

        Returns:
            bytes: The binary representation.

        Raises:
            :exc:`~.exceptions.BadValueException`: If the value does not
                fit the binary format.

        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self.value
        elif 'value' in dir(value):
            # if it is enum or bitmask gets only the 'int' value
            value = value.value

        try:
            return struct.pack(self._fmt, value)
        except struct.error:
            expected_type = type(self).__name__
            actual_type = type(value).__name__
            msg_args = expected_type, value, actual_type
            msg = 'Expected {}, found value "{}" of type {}'.format(*msg_args)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        This method will convert a binary data into a readable value according
        to the attribute format.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.

        """
        try:
            self._value = struct.unpack_from(self._fmt, buff, offset)[0]
            if self.enum_ref:
                self._value = self.enum_ref(self._value)
        except (struct.error, TypeError, ValueError) as exception:
            msg = '{}; fmt = {}, buff = {}, offset = {}.'.format(exception,
                                                                 self._fmt,
                                                                 buff, offset)
            raise UnpackException(msg)

    def get_size(self, value=None):  # pylint: disable=unused-argument
        """Return the size in bytes of this type.

        Returns:
            int: Size in bytes.

        """
        return struct.calcsize(self._fmt)

    def is_valid(self):
        """Check whether the value fits the binary format.

        Assert that :func:`pack` succeeds.

        Returns:
            bool: Whether the value is valid for this type.

        """
        try:
            self.pack()
            return True
        except BadValueException:
            return False

    def isenum(self):
        """Test whether it is an :class:`~enum.Enum`.

        Returns:
            bool: Whether it is an :class:`~enum.Enum`.

        """
        return self.enum_ref and issubclass(self.enum_ref, (Enum, IntEnum))

    def is_bitmask(self):
        """Test whether it is a :class:`GenericBitMask`.

        Returns:
            bool: Whether it is a :class:`GenericBitMask`.

        """
        return self._value and issubclass(type(self._value), GenericBitMask)


class MetaStruct(type):
    """MetaClass that dinamically handles openflow version of class attributes.

    See more about it at:
        https://github.com/kytos/python-openflow/wiki/Version-Inheritance

    You do not need to use this class. Inherit from :class:`GenericStruct`
    instead.
    """

    # pylint: disable=unused-argument
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    def __new__(mcs, name, bases, classdict, **kwargs):
        """Inherit attributes from parent class and update their versions.

        Here is the moment that the new class is going to be created. During
        this process, two things may be done.

        Firstly, we will look if the type of any parent classes is this
        MetaStruct. We will inherit from the first parent class that fits this
        requirement. If any is found, then we will get all attributes from this
        class and place them as class attributes on the class being created.

        Secondly, for each class attribute being inherited, we will make sure
        that the pyof version of this attribute is the same as the version of
        the current class being created. If it is not, then we will find out
        which is the class and module of that attribute, look for a version
        that matches the version of the current class and replace that
        attribute with the correct version.

        See this link for more information on why this is being done:
            - https://github.com/kytos/python-openflow/wiki/Version-Inheritance
        """
        #: Retrieving class attributes management markers
        removed_attributes = classdict.pop('_removed_attributes', [])
        # renamed_attributes = classdict.pop('_renamed_attributes', [])
        # reordered_attributes = classdict.pop('_reordered_attributes', {})

        curr_module = classdict.get('__module__')
        curr_version = MetaStruct.get_pyof_version(curr_module)

        inherited_attributes = None

        #: looking for (kytos) class attributes defined on the bases
        #: classes so we can copy them into the current class being created
        #: so we can "inherit" them as class attributes
        for base in bases:
            #: Check if we are inheriting from one of our classes.
            if isinstance(base, MetaStruct):
                inherited_attributes = OrderedDict()
                for attr_name, obj in base.get_class_attributes():
                    #: Get an updated version of this attribute,
                    #: considering the version of the current class being
                    #: created.
                    attr = MetaStruct.get_pyof_obj_new_version(attr_name, obj,
                                                               curr_version)

                    if attr_name == 'header':
                        attr = mcs._header_message_type_update(obj, attr)

                    inherited_attributes.update([attr])
                #: We are going to inherit just from the 'closest parent'
                break

        #: If we have inherited something, then first we will remove the
        #: attributes marked to be removed on the 'removed_attributes' and
        #: after that we will update the inherited 'classdict' with the
        #: attributes from the current classdict.
        if inherited_attributes is not None:
            #: removing attributes set to be removed
            for attr_name in removed_attributes:
                inherited_attributes.pop(attr_name, None)

            #: Updating the inherited attributes with those defined on the
            #: body of the class being created.
            inherited_attributes.update(classdict)
            classdict = inherited_attributes

        return super().__new__(mcs, name, bases, classdict, **kwargs)

    @staticmethod
    def _header_message_type_update(obj, attr):
        """Update the message type on the header.

        Set the message_type of the header according to the message_type of
        the parent class.
        """
        old_enum = obj.message_type
        new_header = attr[1]
        new_enum = new_header.__class__.message_type.enum_ref
        #: This 'if' will be removed on the future with an
        #: improved version of __init_subclass__ method of the
        #: GenericMessage class
        if old_enum:
            msg_type_name = old_enum.name
            new_type = new_enum[msg_type_name]
            new_header.message_type = new_type
        return (attr[0], new_header)

    @staticmethod
    def get_pyof_version(module_fullname):
        """Get the module pyof version based on the module fullname.

        Args:
            module_fullname (str): The fullname of the module
                (e.g.: pyof.v0x01.common.header)

        Returns:
            str: openflow version.
                 The openflow version, on the format 'v0x0?' if any. Or None
                 if there isn't a version on the fullname.

        """
        ver_module_re = re.compile(r'(pyof\.)(v0x\d+)(\..*)')
        matched = ver_module_re.match(module_fullname)
        if matched:
            version = matched.group(2)
            return version
        return None

    @staticmethod
    def replace_pyof_version(module_fullname, version):
        """Replace the OF Version of a module fullname.

        Get's a module name (eg. 'pyof.v0x01.common.header') and returns it on
        a new 'version' (eg. 'pyof.v0x02.common.header').

        Args:
            module_fullname (str): The fullname of the module
                                   (e.g.: pyof.v0x01.common.header)
            version (str): The version to be 'inserted' on the module fullname.

        Returns:
            str: module fullname
                 The new module fullname, with the replaced version,
                 on the format "pyof.v0x01.common.header". If the requested
                 version is the same as the one of the module_fullname or if
                 the module_fullname is not a 'OF version' specific module,
                 returns None.

        """
        module_version = MetaStruct.get_pyof_version(module_fullname)
        if not module_version or module_version == version:
            return None

        return module_fullname.replace(module_version, version)

    @staticmethod
    def get_pyof_obj_new_version(name, obj, new_version):
        r"""Return a class attribute on a different pyof version.

        This method receives the name of a class attribute, the class attribute
        itself (object) and an openflow version.
        The attribute will be evaluated and from it we will recover its class
        and the module where the class was defined.
        If the module is a "python-openflow version specific module" (starts
        with "pyof.v0"), then we will get it's version and if it is different
        from the 'new_version', then we will get the module on the
        'new_version', look for the 'obj' class on the new module and return
        an instance of the new version of the 'obj'.

        Example:

        >>> from pyof.foundation.base import MetaStruct as ms
        >>> from pyof.v0x01.common.header import Header
        >>> name = 'header'
        >>> obj = Header()
        >>> new_version = 'v0x04'
        >>> header, obj2 = ms.get_pyof_obj_new_version(name, obj, new_version)
        >>> header
        'header'
        >>> obj.version
        UBInt8(1)
        >>> obj2.version
        UBInt8(4)

        Args:
            name (str): the name of the class attribute being handled.
            obj (object): the class attribute itself
            new_version (string): the pyof version in which you want the object
                'obj'.

        Return:
            (str, obj): Tuple with class name and object instance.
                A tuple in which the first item is the name of the class
                attribute (the same that was passed), and the second item is a
                instance of the passed class attribute. If the class attribute
                is not a pyof versioned attribute, then the same passed object
                is returned without any changes. Also, if the obj is a pyof
                versioned attribute, but it is already on the right version
                (same as new_version), then the passed obj is return.

        """
        if new_version is None:
            return (name, obj)

        cls = obj.__class__
        cls_name = cls.__name__
        cls_mod = cls.__module__

        #: If the module name does not starts with pyof.v0 then it is not a
        #: 'pyof versioned' module (OpenFlow specification defined), so we do
        #: not have anything to do with it.
        new_mod = MetaStruct.replace_pyof_version(cls_mod, new_version)
        if new_mod is not None:
            # Loads the module
            new_mod = importlib.import_module(new_mod)
            #: Get the class from the loaded module
            new_cls = getattr(new_mod, cls_name)
            #: return the tuple with the attribute name and the instance
            return (name, new_cls())

        return (name, obj)


class GenericStruct(object, metaclass=MetaStruct):
    """Class inherited by all OpenFlow structs.

    If you need to insert a method that will be used by all structs, this is
    the place to code it.

    .. note:: A struct on this library's context is like a struct in C. It
              has a list of attributes and theses attributes can be structs,
              too.
    """

    def __init__(self):
        """Contructor takes no argument and stores attributes' deep copies."""
        for name, value in self.get_class_attributes():
            setattr(self, name, deepcopy(value))

    def __eq__(self, other):
        """Check whether two structures have the same structure and values.

        Compare the binary representation of structs to decide whether they
        are equal or not.

        Args:
            other (GenericStruct): The struct to be compared with.

        Returns:
            bool: Returns the result of comparation.

        """
        return self.pack() == other.pack()

    @staticmethod
    def _attr_fits_into_class(attr, cls):
        if not isinstance(attr, cls):
            try:
                struct.pack(cls._fmt, attr)  # pylint: disable=protected-access
            except struct.error:
                return False
        return True

    @staticmethod
    def _is_pyof_attribute(obj):
        """Return True if the object is a kytos attribute.

        To be a kytos attribute the item must be an instance of either
        GenericType or GenericStruct.

        Returns:
            bool: Returns TRUE if the obj is a kytos attribute, otherwise False

        """
        return isinstance(obj, (GenericType, GenericStruct))

    def _validate_attributes_type(self):
        """Validate the type of each attribute."""
        for _attr, _class in self._get_attributes():
            if isinstance(_attr, _class):
                return True
            elif issubclass(_class, GenericType):
                if GenericStruct._attr_fits_into_class(_attr, _class):
                    return True
            elif not isinstance(_attr, _class):
                return False
        return True

    @classmethod
    def get_class_attributes(cls):
        """Return a generator for class attributes' names and value.

        This method strict relies on the PEP 520 (Preserving Class Attribute
        Definition Order), implemented on Python 3.6. So, if this behaviour
        changes this whole lib can loose its functionality (since the
        attributes order are a strong requirement.) For the same reason, this
        lib will not work on python versions earlier than 3.6.

        .. code-block:: python3

            for name, value in self.get_class_attributes():
                print("attribute name: {}".format(name))
                print("attribute type: {}".format(value))

        Returns:
            generator: tuples with attribute name and value.

        """
        #: see this method docstring for a important notice about the use of
        #: cls.__dict__
        for name, value in cls.__dict__.items():
            # gets only our (kytos) attributes. this ignores methods, dunder
            # methods and attributes, and common python type attributes.
            if GenericStruct._is_pyof_attribute(value):
                yield (name, value)

    def _get_instance_attributes(self):
        """Return a generator for instance attributes' name and value.

        .. code-block:: python3

            for _name, _value in self._get_instance_attributes():
                print("attribute name: {}".format(_name))
                print("attribute value: {}".format(_value))

        Returns:
            generator: tuples with attribute name and value.

        """
        for name, value in self.__dict__.items():
            if name in map((lambda x: x[0]), self.get_class_attributes()):
                yield (name, value)

    def _get_attributes(self):
        """Return a generator for instance and class attribute.

        .. code-block:: python3

            for instance_attribute, class_attribute in self._get_attributes():
                print("Instance Attribute: {}".format(instance_attribute))
                print("Class Attribute: {}".format(class_attribute))

        Returns:
            generator: Tuples with instance attribute and class attribute

        """
        return map((lambda i, c: (i[1], c[1])),
                   self._get_instance_attributes(),
                   self.get_class_attributes())

    def _get_named_attributes(self):
        """Return generator for attribute's name, instance and class values.

        Add attribute name to meth:`_get_attributes` for a better debugging
        message, so user can find the error easier.

        Returns:
            generator: Tuple with attribute's name, instance and class values.

        """
        for cls, instance in zip(self.get_class_attributes(),
                                 self._get_instance_attributes()):
            attr_name, cls_value = cls
            instance_value = instance[1]
            yield attr_name, instance_value, cls_value

    def _unpack_attribute(self, name, obj, buff, begin):
        attribute = deepcopy(obj)
        setattr(self, name, attribute)
        if not buff:
            size = 0
        else:
            try:
                attribute.unpack(buff, begin)
                size = attribute.get_size()
            except UnpackException as exception:
                child_cls = type(self).__name__
                msg = '{}.{}; {}'.format(child_cls, name, exception)
                raise UnpackException(msg)
        return size

    def get_size(self, value=None):
        """Calculate the total struct size in bytes.

        For each struct attribute, sum the result of each one's ``get_size()``
        method.

        Args:
            value: In structs, the user can assign other value instead of a
                class' instance.

        Returns:
            int: Total number of bytes used by the struct.

        Raises:
            Exception: If the struct is not valid.

        """
        if value is None:
            return sum(cls_val.get_size(obj_val) for obj_val, cls_val in
                       self._get_attributes())
        elif isinstance(value, type(self)):
            return value.get_size()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def pack(self, value=None):
        """Pack the struct in a binary representation.

        Iterate over the class attributes, according to the
        order of definition, and then convert each attribute to its byte
        representation using its own ``pack`` method.

        Returns:
            bytes: Binary representation of the struct object.

        Raises:
            :exc:`~.exceptions.ValidationError`: If validation fails.

        """
        if value is None:
            if not self.is_valid():
                error_msg = "Error on validation prior to pack() on class "
                error_msg += "{}.".format(type(self).__name__)
                raise ValidationError(error_msg)
            else:
                message = b''
                # pylint: disable=no-member
                for attr_info in self._get_named_attributes():
                    name, instance_value, class_value = attr_info
                    try:
                        message += class_value.pack(instance_value)
                    except PackException as pack_exception:
                        cls = type(self).__name__
                        msg = f'{cls}.{name} - {pack_exception}'
                        raise PackException(msg)
                return message
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into this object's attributes.

        Update this object attributes based on the unpacked values of *buff*.
        It is an inplace method and it receives the binary data of the struct.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for name, value in self.get_class_attributes():
            size = self._unpack_attribute(name, value, buff, begin)
            begin += size

    def is_valid(self):
        """Check whether all struct attributes in are valid.

        This method will check whether all struct attributes have a proper
        value according to the OpenFlow specification. For instance, if you
        have a struct with an attribute of type
        :class:`~pyof.foundation.basic_types.UBInt8` and you assign a string
        value to it, this method will return False.

        Returns:
            bool: Whether the struct is valid.

        """
        return True
        # pylint: disable=unreachable
        return self._validate_attributes_type()


class GenericMessage(GenericStruct):
    """Base class that is the foundation for all OpenFlow messages.

    To add a method that will be used by all messages, write it here.

    .. note:: A Message on this library context is like a Struct but has a
              also a :attr:`header` attribute.
    """

    header = None

    def __init__(self, xid=None):
        """Initialize header's xid."""
        super().__init__()
        self.header.xid = randint(0, MAXID) if xid is None else xid

    def __repr__(self):
        """Show a full representation of the object."""
        return "%s(xid=%r)" % (self.__class__.__name__,
                               self.header.xid if self.header else None)

    def __init_subclass__(cls, **kwargs):
        if cls.header is None or cls.header.__class__.__name__ != 'Header':
            msg = "The header attribute must be implemented on the class "
            msg += cls.__name__ + "."
            raise NotImplementedError(msg)
        super().__init_subclass__(**kwargs)

    def _validate_message_length(self):
        return self.header.length == self.get_size()

    def is_valid(self):
        """Check whether a message is valid or not.

        This method will validate the Message content. During the validation
        process, we check whether the attributes' values are valid according to
        the OpenFlow specification. Call this method if you want to verify
        whether the message is ready to pack.

        Returns:
            bool: Whether the message is valid.

        """
        return True
        # pylint: disable=unreachable
        return super().is_valid() and self._validate_message_length()

    def pack(self, value=None):
        """Pack the message into a binary data.

        One of the basic operations on a Message is the pack operation. During
        the packing process, we convert all message attributes to binary
        format.

        Since that this is usually used before sending the message to a switch,
        here we also call :meth:`update_header_length`.

        .. seealso:: This method call its parent's :meth:`GenericStruct.pack`
            after :meth:`update_header_length`.

        Returns:
            bytes: A binary data thats represents the Message.

        Raises:
            Exception: If there are validation errors.

        """
        if value is None:
            self.update_header_length()
            return super().pack()
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for name, value in self.get_class_attributes():
            if type(value).__name__ != "Header":
                size = self._unpack_attribute(name, value, buff, begin)
                begin += size

    def update_header_length(self):
        """Update the header length attribute based on current message size.

        When sending an OpenFlow message we need to inform the message length
        on the header. This is mandatory.
        """
        self.header.length = self.get_size()


class MetaBitMask(type):
    """MetaClass to create a special BitMaskEnum type.

    You probably do not need to use this class. Inherit from
    :class:`GenericBitMask` instead.

    This metaclass converts the declared class attributes into elements of an
    enum. It also replaces the :meth:`__dir__` and :meth:`__getattr__` methods,
    so the resulting class will behave as an :class:`~Enum` class (you can
    access object.ELEMENT and recover either values or names).
    """

    def __new__(mcs, name, bases, classdict):
        """Convert class attributes into enum elements."""
        _enum = OrderedDict([(key, value) for key, value in classdict.items()
                             if key[0] != '_' and not
                             hasattr(value, '__call__') and not
                             isinstance(value, property)])
        if _enum:
            classdict = {key: value for key, value in classdict.items()
                         if key[0] == '_' or hasattr(value, '__call__') or
                         isinstance(value, property)}
            classdict['_enum'] = _enum
        return type.__new__(mcs, name, bases, classdict)

    def __getattr__(cls, name):
        return cls._enum[name]

    def __dir__(cls):
        res = dir(type(cls)) + list(cls.__dict__.keys())
        if cls is not GenericBitMask:
            res.extend(cls._enum)
        return res


class GenericBitMask(object, metaclass=MetaBitMask):
    """Base class for enums that use bitmask values."""

    def __init__(self, bitmask=None):
        """Create a GenericBitMask with the optional parameter below.

        Args:
            bitmask: Bitmask value.
        """
        self.bitmask = bitmask
        self._enum = {}

    def __str__(self):
        return "{}".format(self.bitmask)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.bitmask)

    @property
    def names(self):
        """List of selected enum names.

        Returns:
            list: Enum names.

        """
        result = []
        for key, value in self.iteritems():
            if value & self.bitmask:
                result.append(key)
        return result

    def iteritems(self):
        """Create a generator for attributes' name-value pairs.

        Returns:
            generator: Attributes' (name, value) tuples.

        """
        for key, value in self._enum.items():
            yield (key, value)
