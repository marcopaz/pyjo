no_default = object()


class Field(object):
    _type = None
    _repr = False  # show value in string representation of the python object
    _editable = True
    _attr_name = None  # name of the attribute for which the field is used

    def __init__(self, default=no_default, editable=True, type=None,
                 to_pyjson=None, from_pyjson=None, repr=False):
        """
        :type default: T
        :type type: U
        :rtype: T | U
        """
        self._type = type
        self._repr = repr
        self._editable = editable
        self._to_pyjson = to_pyjson
        self._from_pyjson = from_pyjson
        self._default = default

    @property
    def default(self):
        return None if self._default == no_default else self._default

    @property
    def required(self):
        return self._default == no_default

    def has_default(self):
        return self._default != no_default

    def check_value(self, value):
        if not self.required and value is None:
            return True
        if isinstance(self._type, type):
            if not isinstance(value, self._type):
                return False
        elif callable(self._type):
            if not self._type(value):
                return False
        return True

    def _patch_value(self, value):
        return value

    def to_pyjson(self, value):
        if self._to_pyjson is not None:
            return self._to_pyjson(value)
        if isinstance(value, object) and hasattr(value, 'to_pyjson'):
            return value.to_pyjson()
        return value

    def from_pyjson(self, value):
        if self._from_pyjson is not None:
            return self._from_pyjson(value)
        if self._type and hasattr(self._type, 'from_pyjson'):
            return self._type.from_pyjson(value)
        return value

    def __repr__(self):
        return '<{}(name={})>'.format(
            self.__class__.__name__, self._attr_name)
