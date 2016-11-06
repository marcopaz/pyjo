no_default = object()


class Field(object):
    type = None
    repr = False  # show value in string representation of the python object
    editable = True
    attr_name = None  # name of the attribute for which the field is used

    def __init__(self, default=no_default, editable=True, type=None,
                 to_pyjson=None, from_pyjson=None, repr=False):
        """
        :type default: T
        :type type: U
        :rtype: T | U
        """
        self.type = type
        self.repr = repr
        self.editable = editable
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
        if isinstance(self.type, type):
            if not isinstance(value, self.type):
                return False
        elif callable(self.type):
            if not self.type(value):
                return False
        return True

    def patch_value(self, value):
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
        if self.type and hasattr(self.type, 'from_pyjson'):
            return self.type.from_pyjson(value)
        return value

    def __repr__(self):
        return '<{}(name={})>'.format(
            self.__class__.__name__, self.attr_name)
