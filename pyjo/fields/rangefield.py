from pyjo.fields.field import Field


class RangeField(Field):
    def __init__(self, min=None, max=None, **kwargs):
        """
        :rtype: int
        """
        def type_(x):
            return isinstance(x, int) and (min is None or min <= x) and (max is None or max >= x)
        super(RangeField, self).__init__(type=type_, **kwargs)