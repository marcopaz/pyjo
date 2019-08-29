from pyjo.fields.field import Field


class EnumField(Field):
    def __init__(self, enum, use_name=True, **kwargs):
        """
        :type enum: T
        :rtype: T
        """
        super(EnumField, self).__init__(type=enum, **kwargs)
        self.enum_cls = enum
        self.use_name = use_name

    def to_dict(self, value):
        if value is not None:
            return value.name if self.use_name else value.value

    def from_dict(self, name):
        if name is not None:
            return self.enum_cls[name] if self.use_name else self.enum_cls(name)