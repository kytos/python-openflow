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
