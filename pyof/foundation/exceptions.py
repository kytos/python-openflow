"""Exceptions raised by this library."""


class ValidationError(Exception):
    """Can be used directly or inherited by mpre specific validation errors."""

    def __str__(self):
        return "Validation error: " + super().__str__()


class MethodNotImplemented(Exception):
    """Exception to be raised when a method is not implemented."""

    def __str__(self):
        return "Method not yet implemented: " + super().__str__()


class BadValueException(Exception):
    """Attribute has an unexpected value."""

    def __str__(self):
        return "BadValue error: " + super().__str__()


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


class UnpackException(Exception):
    """Error while unpacking."""

    pass


class PackException(Exception):
    """Error while unpacking."""

    def __str__(self):
        return "Pack error: " + super().__str__()
