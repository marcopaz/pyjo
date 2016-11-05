from copy import copy

__all__ = ["Field", "ConstField", "EnumField", "ModelListField"]

no_default = object()


class Field(object):
    type = None
    repr = False  # show value in string representation of the python object
    editable = True

    def __init__(self, default=no_default, editable=True, type=None,
                 to_json=None, from_json=None, repr=False):
        self.type = type
        self.repr = repr
        self.editable = editable
        self._to_json = to_json
        self._from_json = from_json
        self._default = default

    @property
    def default(self):
        return None if self._default == no_default else self._default

    @property
    def required(self):
        return self._default == no_default

    def has_default(self):
        return self._default != no_default

    def to_json(self, value):
        if self._to_json is not None:
            return self._to_json(value)
        return value

    def from_json(self, value):
        if self._from_json is not None:
            return self._from_json(value)
        return value

    def __repr__(self):
        return '<{}(type={}, default={}, repr={})>'.format(
            self.__class__.__name__, self.type, self.default, self.repr)


class ConstField(Field):
    def __init__(self, value, repr=False, _to_json=None, _from_json=None):
        super(ConstField, self).__init__(default=value, editable=False, repr=repr,
                                         to_json=_to_json, from_json=_from_json)

    def __repr__(self):
        return '<{}(value={})>'.format(
            self.__class__.__name__, self.default)


class EnumField(Field):
    def __init__(self, enum, **kwargs):
        super(EnumField, self).__init__(type=enum, **kwargs)
        self.enum_cls = enum

    def to_json(self, value):
        return value.name

    def from_json(self, name):
        return self.enum_cls[name]


class ModelListField(Field):
    def __init__(self, model, add_model_key=False, **kwargs):
        type = lambda x: isinstance(x, list) and all(isinstance(y, model) for y in x)
        super(ModelListField, self).__init__(type=type, **kwargs)
        self.model = model
        self.add_model_key = add_model_key

    def to_json(self, value):
        if self._to_json is not None:
            return self._to_json(value)
        res = []
        for x in value:
            v = copy(x.to_json())
            if self.add_model_key:
                v["__model__"] = str(x.__class__.__name__)
            res.append(v)
        return res

    def from_json(self, value):
        if self._from_json is not None:
            return self._from_json(value)
        return [self.model.from_json(x) for x in value]
