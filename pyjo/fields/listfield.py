from pyjo.exceptions import FieldTypeError, ValidationError
from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, subtype=None, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=list, **kwargs)
        self._subtype = subtype or object

    def to_pyjson(self, value):
        if self._to_pyjson is not None:
            return self._to_pyjson(value)
        res = []
        for x in value:
            if hasattr(x, 'to_pyjson'):
                x = x.to_pyjson()
            res.append(x)
        return res

    def from_pyjson(self, value):
        if self._from_pyjson is not None:
            return self._from_pyjson(value)
        res = []
        for x in value:
            if hasattr(self._subtype, 'from_pyjson'):
                x = self._subtype.from_pyjson(x)
            res.append(x)
        return res