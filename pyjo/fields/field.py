from pyjo.exceptions import FieldTypeError, ValidationError

orig_type = type


class Field(object):
    name = None

    _type = None
    _repr = False  # show value in string representation of the python object

    def __init__(self, default=None, required=False, type=None, validator=None, to_dict=None, from_dict=None,
                 repr=False):
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
        self._to_dict = to_dict
        self._from_dict = from_dict
        self._default = default
        self._required = required

    def __get__(self, instance, owner):
        if instance is None:
            # Document class being used rather than a document object
            return self

        value = instance._data.get(self.name)
        return value

    def __set__(self, instance, value):
        self.validate(value, instance=instance)
        instance._data[self.name] = value

    def __delete__(self, instance):
        # NOTE: we may want to keep the default value in this case, TBD
        try:
            del instance._data[self.name]
        except KeyError:
            pass

    @property
    def default(self):
        return self._default

    @property
    def required(self):
        return self._required

    def has_default(self):
        return self._default is not None

    def has_value(self, instance):
        return instance._data.get(self.name) is not None

    def validate(self, value, instance=None):
        if not self.required and value is None:
            return
        if self._type is not None and not isinstance(value, self._type):
            raise FieldTypeError(
                '{} value is not of type {}, given {}'.format(self.name, self._type.__name__, value))
        if self._validator:
            try:
                res = self._validator(value)
            except ValidationError as e:
                if e.field_name is None:
                    raise ValidationError('{} did not pass the validation: {}'.format(self.name, e.message),
                                          field_name=self.name)
                else:
                    raise

            if res is False:
                raise ValidationError('{} did not pass the validation'.format(self.name))
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
            self.__class__.__name__, self.name)
