import json

from pyjo.exceptions import RequiredFieldError, NotEditableField
from pyjo.fields.field import Field, no_value, no_default

__all__ = ["Model"]


class Model(object):
    def __init__(self, **kwargs):
        kwargs = self._set_defaults(**kwargs)
        self._check_required_attributes(**kwargs)
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def _set_defaults(self, **kwargs):
        fields = self._get_fields()
        for name, field in fields.items():
            try:
                value = kwargs[name]
            except KeyError:
                value = no_value
            if value is no_value and field.default != no_default:
                if callable(field.default):
                    value = field.default()
                else:
                    value = field.default
            kwargs[name] = value
        return kwargs

    def _check_required_attributes(self, **kwargs):
        fields = self._get_fields()
        for name, field in fields.items():
            try:
                value = kwargs.get(name)
            except KeyError:
                value = no_value
            if field.required and value is no_value:
                raise RequiredFieldError('Field \'{}\' is required'.format(name))

    @classmethod
    def _get_fields(cls):
        fields = {}
        # handle parent classes
        for base in cls.__bases__:
            if issubclass(base, Model):
                fields.update(base._get_fields())
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

    def has_value(self, key):
        return hasattr(self, self._field_attr_value(key)) and getattr(self, self._field_attr_value(key)) is not no_value

    def __setattr__(self, key, value):
        attr = None
        try:
            attr = object.__getattribute__(self, key)
        except AttributeError:
            pass
        if attr is not None and isinstance(attr, Field):
            attr._attr_name = '{}.{}'.format(self.__class__.__name__, key)
            if not attr._editable and hasattr(self, self._field_attr_value(key)):
                raise NotEditableField(key)
            attr.check_value(value)
            return object.__setattr__(self, self._field_attr_value(key), value)
        object.__setattr__(self, key, value)

    def __getattribute__(self, attr):
        value = object.__getattribute__(self, attr)
        if isinstance(value, Field):
            value = object.__getattribute__(self, self._field_attr_value(attr))
        return value

    @classmethod
    def from_dict(cls, value, discard_non_fields=True):
        if not isinstance(value, dict):
            raise TypeError('must be a dict')
        fields = cls._get_fields()
        field_values = {}
        for name, field in fields.items():
            if value.get(name) is not None:
                field_values[name] = field.from_dict(value[name])
        if discard_non_fields:
            value = field_values
        else:
            value.update(field_values)
        return cls(**value)

    def update_from_dict(self, value, discard_non_fields=True):
        if not isinstance(value, dict):
            raise TypeError('must be a dict')
        fields = self._get_fields()
        field_values = {}
        for name, field in fields.items():
            if value.get(name) is not None:
                field_values[name] = field.from_dict(value[name])
        if discard_non_fields:
            value = field_values
        else:
            value.update(field_values)

        for k,v in value.items():
            setattr(self, k, v)

        return self

    def to_dict(self):
        fields = self._get_fields()
        res = {}
        for name, field in fields.items():
            try:
                value = getattr(self, name)
            except AttributeError:
                value = None
            if value is not no_value:
                res[name] = field.to_dict(value)
        return res

    @classmethod
    def from_json(cls, value, discard_non_fields=True):
        v = json.loads(value)
        return cls.from_dict(v, discard_non_fields=discard_non_fields)

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)

    def __repr__(self):
        fields = self._get_fields()

        res = []
        for name, field in fields.items():
            if not field._repr:
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
