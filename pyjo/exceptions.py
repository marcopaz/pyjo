class Error(Exception):
    pass


class RequiredField(Error):
    def __init__(self, field_name):
        message = 'Field \'{}\' is required'.format(field_name)
        super(RequiredField, self).__init__(message)


class InvalidType(Error):
    def __init__(self, field_name, type, value):
        message = 'The value of the field \'{}\' is not of type {}, given {}'.format(field_name, type, value)
        super(InvalidType, self).__init__(message)


class NotEditableField(Error):
    def __init__(self, field_name):
        message = 'The value of the field \'{}\' is not editable'.format(field_name)
        super(NotEditableField, self).__init__(message)
