"""Base and fundamental classes used all over the library.

Besides classes, several constants are defined here. We designed
python-openflow in a manner to make it easy to create new messages and OpenFlow
structs. You can realize that when you see a message class definition.

A **struct** here is a group of basic attributes and/or struct attributes (i.e.
:class:`~.common.header.Header`). A **message** here is like a struct, but all
messages have a header attribute (i.e.
:class:`~.asynchronous.packet_in.PacketIn`).

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
from enum import Enum

# Local source tree imports
from pyof.foundation.exceptions import (BadValueException, PackException,
                                        UnpackException, ValidationError)

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
        """The constructor takes the optional parameters below.

        Args:
            value: The type's value.
            enum_ref (:class:`type`): If :attr:`value` is from an Enum, specify
                its type.
        """
        self._value = value
        self.enum_ref = enum_ref

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
        return self._value <= other

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

    @property
    def value(self):
        """Return this type's value.

        The value of an enum, bitmask, etc.
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
            msg = '{} could not pack {} = {}.'.format(type(self).__name__,
                                                      type(value).__name__,
                                                      value)
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
        except (struct.error, TypeError, ValueError) as e:
            msg = '{}; fmt = {}, buff = {}, offset = {}.'.format(e, self._fmt,
                                                                 buff, offset)
            raise UnpackException(msg)

    def get_size(self, value=None):
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
        """Test whether it is an :class:`~Enum`.

        Returns:
            bool: Whether it is an :class:`~Enum`.
        """
        return self.enum_ref and issubclass(self.enum_ref, Enum)

    def is_bitmask(self):
        """Test whether it is a :class:`GenericBitMask`.

        Returns:
            bool: Whether it is a :class:`GenericBitMask`.
        """
        return self._value and issubclass(type(self._value), GenericBitMask)


class MetaStruct(type):
    """MetaClass to force ordered attributes.

    You probably do not need to use this class. Inherit from
    :class:`GenericStruct` instead.
    """

    @classmethod
    def __prepare__(mcs, name, bases):  # pylint: disable=unused-argument
        return OrderedDict()

    def __new__(mcs, name, bases, classdict):
        """Add ``__ordered__`` attribute with attributes in declared order."""
        ordered = None

        #: Recovering __ordered__ from the first parent class that have it,
        #: if any
        for base in bases:
            if hasattr(base, '__ordered__'):
                # TODO: How to do a "copy from current of version" that get the
                #       class (value) from the correct pyof version (the same
                #       as the class being edited/created)?
                #       This is where we need to do some magic!
                #: Try to get the __ordered__ dict from the base (parent) class.
                #: If it fails (there is no __ordered__) then an exception is
                #: raised
                base_ordered = base.__ordered__.copy()

                #: List with attributes names to be removed.
                remove_attributes = classdict.get('_remove_attributes')

                #: List of tuples like (old_name, new_name)
                rename_attributes = classdict.get('_rename_attributes')

                #: A dict with new_attribute_name as key and valued with the
                #: name of the attribute that will be preceeded by this new
                #: attribute.
                insert_before = classdict.get('_insert_attributes_before')

                # Remove attributes marked to be removed, if any to do so
                if remove_attributes is not None:
                    for attr in remove_attributes:
                        try:
                            base_ordered.pop(attr)
                        except KeyError:
                            pass

                # Renaming attributes copied from the parent class
                if rename_attributes is not None:
                    for old_name, new_name in rename_attributes:
                        if old_name in classdict:
                            classdict[new_name] = classdict.pop(old_name)
                        else:
                            classdict[new_name] = deepcopy(base.__dict__[old_name])
                        base_ordered = OrderedDict([(new_name, v) if
                                                    k == old_name else (k, v)
                                                    for k, v in
                                                    base_ordered.items()])

                # Now let's get the new class attributes.
                new_attrs = OrderedDict([(key, type(value)) for
                                         key, value in classdict.items()
                                         if key[0] != '_' and not
                                         hasattr(value, '__call__')])

                attrs = list(base_ordered.keys())

                # And now lets add these new attributes to the ordered dict,
                # considering the insert_before item data.
                for attr in list(new_attrs.keys()):
                    #: If the attribute was redefined, by default we will
                    #: keep it at the same place it was before. So, we do not
                    #: need to add it again.
                    if attr not in attrs:
                        if insert_before and attr in insert_before:
                            #: If the attribute must be added before some other
                            #: attribute, do so.
                            attrs.insert(attrs.index(insert_before[attr]),
                                         attr)
                        else:
                            #: Otherwise append the new attribute into the end
                            #: of the list
                            attrs.append(attr)

                #: finally creating the ordered dict that will be added on the
                #: class.
                ordered = OrderedDict()
                for attr in attrs:
                    ordered[attr] = new_attrs.get(attr, base_ordered.get(attr))

                #: break the for loop, we are just interested on the first
                #: base class that have the __ordered__ dict.
                break

        if ordered is None:
            #: If there was no __ordered__ dict on the parent class, create
            #: one with the current class attributes, skipping methods and
            #: private attributes
            ordered = OrderedDict([(key, type(value)) for
                                   key, value in classdict.items()
                                   if key[0] != '_' and not
                                   hasattr(value, '__call__')])

        classdict['__ordered__'] = ordered

        return type.__new__(mcs, name, bases, classdict)

    @staticmethod
    def get_pyof_version(module_fullname):
        """Get the module pyof version based on the module fullname.

        Args:
            module_fullname (str): The fullname of the module
                (e.g.: pyof.v0x01.common.header)

        Returns:
            version (str): The module version, on the format 'v0x0?' if any. Or
            None (None): If there isn't a version on the fullname.
        """
        ver_module_re = re.compile(r'(pyof\.)(v0x\d+)(\..*)')
        matched = ver_module_re.match(module_fullname)
        if matched:
            version = matched.group(2)
            # module = matched.group(3)
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
            None (None): if the requested version is the same as the one of the
                module_fullname or if the module_fullname is not a 'OF version'
                specific module.
            new_module_fullname (str): The new module fullname, with the
                replaced version, on the format "pyof.v0x01.common.header".
        """
        module_version = MetaStruct.get_pyof_version(module_fullname)
        if not module_version or module_version == version:
            return None
        else:
            return module_fullname.replace(module_version, version)

    @staticmethod
    def get_pyof_obj_new_version(name, obj, new_version):
        """Return a class atrribute on a different pyof version.

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
            >> from pyof.v0x01.common.header import Header
            >> name = 'header'
            >> obj = Header()
            >> obj
            <pyof.v0x01.common.header.Header at 0x...>
            >> new_version = 'v0x02'
            >> MetaStruct.get_pyof_new_version(name, obj, new_version)
            ('header', <pyof.v0x02.common.header.Header at 0x...)

        Args:
            name (str): the name of the class attribute being handled.
            obj (object): the class attribute itself
            new_version (string): the pyof version in which you want the object
                'obj'.

        Return:
            (name, obj): A tuple in which the first item is the name of the
                class attribute (the same that was passed), and the second item
                is a instance of the passed class attribute. If the class
                attribute is not a pyof versioned attribute, then the same
                passed object is returned without any changes. Also, if the obj
                is a pyof versioned attribute, but it is already on the right
                version (same as new_version), then the passed obj is return.
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
        for name, value in self._get_class_attributes():
            setattr(self, name, deepcopy(value))

    def __eq__(self, other):
        """Check whether two structures have the same structure and values.

        Compare the binary representation of structs to decide whether they
        are equal or not.

        Args:
            other (GenericStruct): The struct to be compared with.
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

        returns:
            True: if the obj is a kytos attribute
            False: if the obj is not a kytos attribute
        """
        return isinstance(obj, GenericType) or isinstance(obj, GenericStruct)

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
    def _get_class_attributes(cls):
        """Return a generator for class attributes' names and value.

        This method strict relies on the PEP 520 (Preserving Class Attribute
        Definition Order), implemented on Python 3.6. So, if this behaviour
        changes this whole lib can loose its functionality (since the
        attributes order are a strong requirement.) For the same reason, this
        lib will not work on python versions earlier than 3.6.

        .. code-block:: python3

            for _name, _value in self._get_class_attributes():
                print("attribute name: {}".format(_name))
                print("attribute type: {}".format(_value))

        returns:
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

        returns:
            generator: tuples with attribute name and value.
        """
        for name, value in self.__dict__.items():
            if name in map((lambda x: x[0]), self._get_class_attributes()):
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
                   self._get_class_attributes())

    def _unpack_attribute(self, name, obj, buff, begin):
        attribute = deepcopy(obj)
        setattr(self, name, attribute)
        if len(buff) == 0:
            size = 0
        else:
            try:
                attribute.unpack(buff, begin)
                size = attribute.get_size()
            except UnpackException as e:
                child_cls = type(self).__name__
                msg = '{}.{}; {}'.format(child_cls, name, e)
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
            # size = 0
            # for obj_val, cls_val in self.get_attributes():
            #     print('cls_val', cls_val, type(cls_val))
            #     print('obj_val', obj_val, type(obj_val))
            #     print('size is', cls_val.get_size(obj_val))
            #     size += cls_val.get_size(obj_val)
            # return size
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
                for instance_attr, class_attr in self._get_attributes():
                    message += class_attr.pack(instance_attr)
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
        for name, value in self._get_class_attributes():
            size = self._unpack_attribute(name, value, buff, begin)
            begin += size

    def is_valid(self):
        """Check whether all struct attributes in are valid.

        This method will check whether all struct attributes have a proper
        value according to the OpenFlow specification. For instance, if you
        have a struct with an attribute of type :class:`UBInt8()`
        and you assign a string value to it, this method will return False.

        Returns:
            bool: Whether the struct is valid.
        """
        return True
        # pylint: disable=unreachable
        if not self._validate_attributes_type():
            return False
        return True


class GenericMessage(GenericStruct):
    """Base class that is the foundation for all OpenFlow messages.

    To add a method that will be used by all messages, write it here.

    .. note:: A Message on this library context is like a Struct but has a
              also a :attr:`header` attribute.
    """

    header = None

    def __init__(self, xid):
        """Initialize header's xid."""
        super().__init__()
        if xid is not None:
            self.header.xid = xid


    def _validate_message_length(self):
        if not self.header.length == self.get_size():
            return False
        return True

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
        if not super().is_valid():
            return False
        if not self._validate_message_length():
            return False
        return True

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
        for name, value in self._get_class_attributes():
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
        """The constructor has the optional parameter below.

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
        """Generator for attributes' name-value pairs.

        Returns:
            generator: Attributes' (name, value) tuples.
        """
        for key, value in self._enum.items():
            yield (key, value)
