"""Exceptions raised by this library."""


class ValidationError(Exception):
    """Can be used directly or inherited by mpre specific validation errors."""

    pass


class MethodNotImplemented(Exception):
    """Exception to be raised when a method is not implemented."""

    def __init__(self, message=None):
        """The constructor takes an optional message.

        Args:
            message (str): The error message. Defaults to "Method not yet
                implemented".
        """
        super().__init__()
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "Method not yet implemented"


class BadValueException(Exception):
    """Attribute has an unexpected value."""

    pass


class WrongListItemType(Exception):
    """When an item of a wrong type is inserted into a list.

    Exception used by :class:`.FixedTypeList` and :class:`.ConstantTypeList`
    when the user tries to insert an item that does not match the expected
    type.
    """

    def __init__(self, item_class, expected_class):
        """The constructor takes parameters to inform the user about the error.

        Args:
            item_class (:obj:`type`): The class of the item that was being
                inserted in the list when the exception was raised.
            expected_class (:obj:`type`): The expected type that didn't match
                against the item to be inserted.
        """
        super().__init__()
        self.item_class = item_class
        self.expected_class = expected_class

    def __str__(self):
        return "'{}' is not an instance of {}".format(self.item_class,
                                                      self.expected_class)


class NotBinaryData(Exception):
    """The content of a BinaryData attribute is not binary."""

    def __str__(self):
        return "The content of this variable needs to be binary data"


class UnpackException(Exception):
    """Error while unpacking."""

    pass
