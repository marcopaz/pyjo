from pyjo.fields.field import Field


class EnumField(Field):
    def __init__(self, enum, **kwargs):
        """
        :type enum: T
        :rtype: T
        """
        super(EnumField, self).__init__(type=enum, **kwargs)
        self.enum_cls = enum

    def to_dict(self, value):
        if value is not None:
            return value.name

    def from_dict(self, name):
        if name is not None:
            return self.enum_cls[name]
