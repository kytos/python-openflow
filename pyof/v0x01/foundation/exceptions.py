"""Exceptions defined on this Library"""


class Exception(Exception):
    pass


class BadValueException(Exception):
    pass


class NoUnpackException(Exception):
    def __str__(self):
        return "This class has no 'unpack()' method implemented."


class PADHasNoValue(Exception):
    """Exception raised when the user tries to set a value on a PAD attribute
    """
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
        return ("Unexpected value ('{}') on attribute '{}' "
                "from class '{}'".format(self.item,
                                         self.name, self.expected_class))
