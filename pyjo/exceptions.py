class Error(Exception):
    pass


class RequiredField(Error):
    def __init__(self, field_name):
        message = 'Field \'{}\' is required'.format(field_name)
        super(RequiredField, self).__init__(message)


class InvalidType(Error):
    def __init__(self, attr_name, type, value):
        message = 'The value of the field \'{}\' is not of type {}, given {}'.format(attr_name, type.__name__, value)
        super(InvalidType, self).__init__(message)


class InvalidValue(Error):
    def __init__(self, attr_name, value):
        message = 'The value of the field \'{}\' did not pass the validation, given {}'.format(attr_name, value)
        super(InvalidValue, self).__init__(message)


class NotEditableField(Error):
    def __init__(self, field_name):
        message = 'The value of the field \'{}\' is not editable'.format(field_name)
        super(NotEditableField, self).__init__(message)
