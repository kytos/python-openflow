"""Exceptions defined on this Library"""


class MethodNotImplemented(Exception):
    """Exception to be raised when a method is not implemented"""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "Method not yet implemented"


class BadValueException(Exception):
    pass


class WrongListItemType(Exception):
    """Exception used for FixedTypeList and ConstantTypeList classes
    instances when the user tries to insert an item on this
    lists that does not match the expected type."""
    def __init__(self, item_class, expected_class):
        self.item_class = item_class
        self.expected_class = expected_class

    def __str__(self):
        message = "'{}' is not an instance of ".format(self.item_class)
        message = message + "type '{}'".format(self.expected_class)
        return message


class PADHasNoValue(Exception):
    """Exception raised when user tries to set a value on a PAD attribute"""
    def __str__(self):
        return "You can't set a value on a PAD attribute"


class AttributeTypeError(Exception):
    """Error raise when the attribute is not of the expected type
    defined on the class definition"""

    def __init__(self, item, item_class, expected_class):
        self.item = item
        self.item_class = item_class
        self.expected_class = expected_class

    def __str__(self):
        msg = "Unexpected value ('{}') ".format(str(self.item))
        msg += "on attribute '{}' ".format(str(self.name))
        msg += "from class '{}'".format(str(self.expected_class))
        return msg


class NotBinaryData(Exception):
    """Error raised when the content of a BinaryData attribute is not binary"""
    def __str__(self):
        return("The content of this variable needs to be binary data")


class ValidationError(Exception):
    """Error on validate message or struct"""
    def __init__(self, msg="Error on validate message"):
        self.msg = msg
    def __str__(self):
        return self.msg


class UnpackException(Exception):
    pass
