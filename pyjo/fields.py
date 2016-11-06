import re
from copy import copy

__all__ = ["Field", "ConstField", "EnumField", "ModelListField", "RegexField", "RangeField"]

no_default = object()


class Field(object):
    type = None
    repr = False  # show value in string representation of the python object
    editable = True

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
        return '<{}(type={}, default={}, repr={})>'.format(
            self.__class__.__name__, self.type, self.default, self.repr)


class ConstField(Field):
    def __init__(self, value, **kwargs):
        """
        :type value: T
        :rtype: T
        """
        kwargs['default'] = value
        kwargs['editable'] = False
        super(ConstField, self).__init__(**kwargs)

    def __repr__(self):
        return '<{}(value={})>'.format(
            self.__class__.__name__, self.default)


class EnumField(Field):
    def __init__(self, enum, **kwargs):
        """
        :type enum: T
        :rtype: T
        """
        super(EnumField, self).__init__(type=enum, **kwargs)
        self.enum_cls = enum

    def to_pyjson(self, value):
        if value is not None:
            return value.name

    def from_pyjson(self, name):
        if name is not None:
            return self.enum_cls[name]


class ModelListField(Field):
    def __init__(self, model, add_model_key=False, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        type = lambda x: isinstance(x, list) and all(isinstance(y, model) for y in x)
        super(ModelListField, self).__init__(type=type, **kwargs)
        self.model = model
        self.add_model_key = add_model_key

    def to_pyjson(self, value):
        if self._to_pyjson is not None:
            return self._to_pyjson(value)
        res = []
        for x in value:
            v = copy(x.to_pyjson())
            if self.add_model_key:
                v["__model__"] = str(x.__class__.__name__)
            res.append(v)
        return res

    def from_pyjson(self, value):
        if self._from_pyjson is not None:
            return self._from_pyjson(value)
        return [self.model.from_pyjson(x) for x in value]


class RegexField(Field):
    def __init__(self, regex, **kwargs):
        def type_(x):
            return isinstance(x, str) and re.match(regex, x)
        super(RegexField, self).__init__(type=type_, **kwargs)


class RangeField(Field):
    def __init__(self, min=None, max=None, **kwargs):
        def type_(x):
            return isinstance(x, int) and (min is None or min <= x) and (max is None or max >= x)
        super(RangeField, self).__init__(type=type_, **kwargs)

