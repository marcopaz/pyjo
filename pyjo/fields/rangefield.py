from pyjo.fields.field import Field


class RangeField(Field):
    def __init__(self, min=None, max=None, **kwargs):
        """
        :rtype: int
        """

        def validator(x):
            return (min is None or min <= x) and (max is None or max >= x)

        super(RangeField, self).__init__(type=int, validator=validator, **kwargs)
