from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, subtype=None, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=list, **kwargs)
        self._subtype = subtype or object

    def to_dict(self, value):
        if self._to_dict is not None:
            return self._to_dict(value)
        res = []
        for x in value:
            if hasattr(x, 'to_dict'):
                x = x.to_dict()
            res.append(x)
        return res

    def from_dict(self, value):
        if self._from_dict is not None:
            return self._from_dict(value)
        res = []
        for x in value:
            if hasattr(self._subtype, 'from_dict'):
                x = self._subtype.from_dict(x)
            res.append(x)
        return res
