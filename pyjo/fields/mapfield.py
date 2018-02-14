from pyjo.fields.field import Field


class MapField(Field):
    def __init__(self, inner_field, **kwargs):
        """
        :type inner_field: T
        :rtype: dict[str, T]
        """
        super(MapField, self).__init__(type=dict, **kwargs)
        self.inner_field = inner_field

    def validate(self, value, **kwargs):
        super(MapField, self).validate(value, **kwargs)
        if not value:
            return
        self.inner_field.name = self.name
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
