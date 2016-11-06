import json
from typing import Dict

from pyjo.exceptions import RequiredField, InvalidType, NotEditableField
from pyjo.fields.field import Field

__all__ = ["Model"]


class Model(object):

    def __init__(self, **kwargs):
        kwargs = self._set_defaults(**kwargs)
        self._check_required_attributes(**kwargs)
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def _set_defaults(self, **kwargs):
        fields = self.get_fields()
        for name, field in fields.items():
            kwargs[name] = kwargs.get(name, field.default)
        return kwargs

    def _check_required_attributes(self, **kwargs):
        fields = self.get_fields()
        for name, field in fields.items():
            value = kwargs.get(name)
            if field.required and value is None:
                raise RequiredField(field_name=name)

    @classmethod
    def get_fields(cls):
        fields = {}
        for attr_name in dir(cls):
            try:
                val = object.__getattribute__(cls, attr_name)
            except AttributeError:
                continue
            if isinstance(val, Field):
                fields[attr_name] = val
        return fields

    @staticmethod
    def _field_attr_value(key):
        return '__field_{}'.format(key)

    def __setattr__(self, key, value):
        attr = None
        try:
            attr = object.__getattribute__(self, key)
        except AttributeError:
            pass
        if attr is not None and isinstance(attr, Field):
            attr.attr_name = key
            if not attr.editable and hasattr(self, self._field_attr_value(key)):
                raise NotEditableField(key)
            if not attr.check_value(value):
                raise InvalidType(attr_name=key, type=attr.type, value=value)
            value = attr.patch_value(value)
            return object.__setattr__(self, self._field_attr_value(key), value)
        object.__setattr__(self, key, value)

    def __getattribute__(self, attr):
        value = object.__getattribute__(self, attr)
        if isinstance(value, Field):
            value = object.__getattribute__(self, self._field_attr_value(attr))
        return value

    @classmethod
    def from_pyjson(cls, value):
        fields = cls.get_fields()
        for name, field in fields.items():
            if value.get(name) is not None:
                value[name] = field.from_pyjson(value[name])
        return cls(**value)

    def to_pyjson(self):
        fields = self.get_fields()
        res = {}
        for name, field in fields.items():
            try:
                value = getattr(self, name)
            except AttributeError:
                value = None
            res[name] = field.to_pyjson(value)
        return res

    @classmethod
    def from_json(cls, value):
        v = json.loads(value)
        return cls.from_pyjson(v)

    def to_json(self, indent=None):
        return json.dumps(self.to_pyjson(), indent=indent)

    def __repr__(self):
        fields = self.get_fields()

        res = []
        for name,field in fields.items():
            if not field.repr:
                continue
            try:
                value = getattr(self, name)
            except AttributeError:
                value = None
            res.append('{}={}'.format(name, value))

        fields = ', '.join(res)
        return '<{}({})>'.format(self.__class__.__name__, fields)


if __name__ == '__main__':
    pass
