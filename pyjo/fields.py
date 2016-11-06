import re

from pyjo.exceptions import InvalidType

__all__ = ["Field", "ConstField", "EnumField", "ListField", "RegexField", "RangeField"]

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


class ListField(Field):
    def __init__(self, subtype, check_elements_type=True, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=self.check_type, **kwargs)
        self.subtype = subtype
        self.check_elements_type = check_elements_type

    def check_subtype(self, value):
        if isinstance(self.subtype, Field):
            return self.subtype.check_value(value)
        else:
            return isinstance(value, self.subtype)

    def check_type(self, value):
        return isinstance(value, list) and (
                    not self.check_elements_type or all(self.check_subtype(x) for x in value))

    def patch_value(self, value):

        class TypedList(list):
            def __setitem__(_self, item_key, item_value):
                if not self.check_subtype(value):
                    raise InvalidType(attr_name=self.attr_name, type=self.check_subtype, value=item_value)
                return super(TypedList, _self).__setitem__(item_key, item_value)

        if self.check_elements_type and hasattr(value, '__setitem__'):
            value = TypedList(value)

        return value

    def to_pyjson(self, value):
        if self._to_pyjson is not None:
            return self._to_pyjson(value)
        res = []
        for x in value:
            if hasattr(x, 'to_pyjson'):
                x = x.to_pyjson()
            res.append(x)
        return res

    def from_pyjson(self, value):
        if self._from_pyjson is not None:
            return self._from_pyjson(value)
        res = []
        for x in value:
            if hasattr(self.subtype, 'from_pyjson'):
                x = self.subtype.from_pyjson(x)
            res.append(x)
        return res


class RegexField(Field):
    def __init__(self, regex, **kwargs):
        """
        :rtype: str
        """
        def type_(x):
            return isinstance(x, str) and re.match(regex, x)
        super(RegexField, self).__init__(type=type_, **kwargs)


class RangeField(Field):
    def __init__(self, min=None, max=None, **kwargs):
        """
        :rtype: int
        """
        def type_(x):
            return isinstance(x, int) and (min is None or min <= x) and (max is None or max >= x)
        super(RangeField, self).__init__(type=type_, **kwargs)
