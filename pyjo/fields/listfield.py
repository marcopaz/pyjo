from pyjo.exceptions import FieldTypeError
from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, inner_field, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=list, **kwargs)
        self.inner_field = inner_field

    def after_name_set(self):
        self.inner_field.name = '{} inner field'.format(self.name)

    def cast(self, value):
        value = super(ListField, self).cast(value)
        if not isinstance(value, list):
            raise FieldTypeError(
                '{} value is not of type {}, given "{}"'.format(self.name, self._type.__name__, value),
                field_name=self.name
            )
        return [self.inner_field.cast(v) for v in value]

    def validate(self, value, **kwargs):
        super(ListField, self).validate(value, **kwargs)
        if not value:
            return
        for v in value:
            self.inner_field.validate(v)

    def to_dict(self, value):
        if value is None:
            return value

        res = []
        for v in value:
            res.append(self.inner_field.to_dict(v))
        return res

    def from_dict(self, value):
        if value is None:
            return value

        res = []
        for v in value:
            res.append(self.inner_field.from_dict(v))
        return res
