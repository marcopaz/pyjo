class Error(Exception):
    field_name = None

    def __init__(self, message, field_name=None):
        super(Error, self).__init__(message)
        self.message = message
        self.field_name = field_name


class RequiredFieldError(Error):
    pass


class FieldTypeError(Error):
    pass


class ValidationError(Error):
    pass


class NotEditableField(Error):
    pass
