import json

from pyjo.exceptions import RequiredFieldError, NotEditableField
from pyjo.fields.field import Field

from six import with_metaclass, iteritems

__all__ = ["ModelMetaclass", "Model"]


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(ModelMetaclass, cls).__new__

        # If a base class just call super
        metaclass = attrs.get('my_metaclass')
        if metaclass and issubclass(metaclass, ModelMetaclass):
            return super_new(cls, name, bases, attrs)

        # Build _fields and assign name

        # Merge all fields from subclasses
        _fields = {}
        flattened_bases = cls._get_bases(bases)
        for base in flattened_bases[::-1]:
            if hasattr(base, '_fields'):
                _fields.update(base._fields)
            fields = {}
            for attr_name, attr_value in iteritems(base.__dict__):
                if not isinstance(attr_value, Field):
                    continue
                attr_value.name = attr_name
                attr_value.after_name()
                fields[attr_name] = attr_value
            _fields.update(fields)

        # Discover any model fields
        for attr_name, attr_value in iteritems(attrs):
            if not isinstance(attr_value, Field):
                continue
            attr_value.name = attr_name
            attr_value.after_name()
            _fields[attr_name] = attr_value

        attrs['_fields'] = _fields

        return super_new(cls, name, bases, attrs)

    @classmethod
    def _get_bases(cls, bases):
        bases = cls.__get_bases(bases)
        unique_bases = list(set(bases))
        return unique_bases

    @classmethod
    def __get_bases(cls, bases):
        for base in bases:
            if base is object:
                continue
            yield base
            for child_base in cls.__get_bases(base.__bases__):
                yield child_base


class Model(with_metaclass(ModelMetaclass, object)):

    my_metaclass = ModelMetaclass

    def __init__(self, **kwargs):
        self._data = {}
        self._set_defaults(kwargs)
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def _set_defaults(self, kwargs):
        for name, field in iteritems(self._fields):
            value = kwargs.get(name)
            if value is None and field.default is not None:
                if callable(field.default):
                    value = field.default()
                else:
                    value = field.default
            kwargs[name] = value

    @classmethod
    def from_dict(cls, data, discard_non_fields=True):
        if not isinstance(data, dict):
            raise TypeError('must be a dict')
        field_values = {}
        for name, field in iteritems(cls._fields):
            value = data.get(name)
            if value is not None:
                field_values[name] = field.from_dict(value)
        if discard_non_fields:
            data = field_values
        else:
            data.update(field_values)
        return cls(**data)

    def update_from_dict(self, data, discard_non_fields=True):
        if not isinstance(data, dict):
            raise TypeError('must be a dict')

        field_values = {}
        for name, field in iteritems(self._fields):
            value = data.get(name)
            field_values[name] = field.from_dict(value)
        if discard_non_fields:
            data = field_values
        else:
            data.update(field_values)

        for k,v in iteritems(data):
            setattr(self, k, v)

    def to_dict(self):
        res = {}
        for name, field in iteritems(self._fields):
            if field.has_value(self):
                value = getattr(self, name)
                res[name] = field.to_dict(value)
        return res

    @classmethod
    def from_json(cls, value, discard_non_fields=True):
        v = json.loads(value)
        return cls.from_dict(v, discard_non_fields=discard_non_fields)

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)

    def __repr__(self):
        res = []
        for name, field in iteritems(self._fields):
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
