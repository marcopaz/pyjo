from pyjo.exceptions import FieldTypeError, ValidationError

no_default = object()
no_value = object()
orig_type = type


class Field(object):
    _type = None
    _repr = False  # show value in string representation of the python object
    _editable = True
    _attr_name = None  # name of the attribute for which the field is used

    def __init__(self, default=no_default, required=False, editable=True, type=None, allow_none=False,
                 validator=None, to_dict=None, from_dict=None, repr=False):
        """
        :type default: T
        :type type: U
        :rtype: T | U
        """

        if type is not None and not isinstance(type, orig_type):
            raise TypeError('Invalid value for type. It should be a type')

        if validator is not None and not callable(validator):
            raise TypeError('Invalid value for validator. It should be callable')

        if repr is not None and not isinstance(repr, bool):
            raise TypeError('Invalid value for repr. It should be a bool')

        if to_dict is not None and not callable(to_dict):
            raise TypeError('Invalid value for to_dict. It should be callable')

        if from_dict is not None and not callable(from_dict):
            raise TypeError('Invalid value for from_dict. It should be callable')

        self._type = type
        self._validator = validator
        self._repr = repr
        self._editable = editable
        self._to_dict = to_dict
        self._from_dict = from_dict
        self._default = default
        self._required = required
        self._allow_none = allow_none

    @property
    def default(self):
        return self._default

    @property
    def required(self):
        return self._required and self._default == no_default

    def has_default(self):
        return self._default != no_default

    def check_value(self, value):
        if not self.required and value is no_value:
            return
        if self._allow_none and value is None:
            return
        if self._type is not None and not isinstance(value, self._type):
            raise FieldTypeError(
                '{} value is not of type {}, given {}'.format(self._attr_name, self._type.__name__, value))
        if self._validator:
            try:
                res = self._validator(value)
            except ValidationError as e:
                if e.field_name is None:
                    raise ValidationError('{} did not pass the validation: {}'.format(self._attr_name, e.message),
                                          field_name=self._attr_name)
                else:
                    raise

            if res is False:
                raise ValidationError('{} did not pass the validation'.format(self._attr_name))
        return

    def to_dict(self, value):
        if self._to_dict is not None:
            return self._to_dict(value)
        if isinstance(value, object) and hasattr(value, 'to_dict'):
            return value.to_dict()
        return value

    def from_dict(self, value):
        if self._from_dict is not None:
            return self._from_dict(value)
        if self._type and hasattr(self._type, 'from_dict'):
            return self._type.from_dict(value)
        return value

    def __repr__(self):
        return '<{}(name={})>'.format(
            self.__class__.__name__, self._attr_name)
