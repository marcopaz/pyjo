from six import iteritems

from pyjo.exceptions import FieldTypeError
from pyjo.fields.field import Field


class MapField(Field):
    def __init__(self, inner_field, **kwargs):
        """
        :type inner_field: T
        :rtype: dict[str, T]
        """
        super(MapField, self).__init__(type=dict, **kwargs)
        self.inner_field = inner_field

    def after_name(self):
        self.inner_field.name = '{} inner field'.format(self.name)

    def cast(self, value):
        value = super(MapField, self).cast(value)
        if not isinstance(value, dict):
            raise FieldTypeError(
                '{} value is not of type {}, given "{}"'.format(self.name, self._type.__name__, value),
                field_name=self.name
            )
        return {k: self.inner_field.cast(v) for k, v in iteritems(value)}

    def validate(self, value, **kwargs):
        super(MapField, self).validate(value, **kwargs)
        if not value:
            return
        for k, v in value.items():
            self.inner_field.validate(v)

    def from_dict(self, value):
        if value is None:
            return value

        res = {}
        for k, v in value.items():
            res[k] = self.inner_field.from_dict(v)
        return res

    def to_dict(self, value):
        if value is None:
            return value

        res = {}
        for k, v in value.items():
            res[k] = self.inner_field.to_dict(v)

        return res
