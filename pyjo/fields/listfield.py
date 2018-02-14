from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, inner_field, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=list, **kwargs)
        self.inner_field = inner_field

    def validate(self, value, **kwargs):
        super(ListField, self).validate(value, **kwargs)
        if not value:
            return
        self.inner_field.name = self.name
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
