"""Exceptions defined on this Library"""


class Exception(Exception):
    pass


class BadValueException(Exception):
    pass


class PADHasNoValue(Exception):
    """Exception raised when the user tries to set a value on a PAD attribute
    """
    def __str__(self):
        return repr('PAD has no value to be set')
