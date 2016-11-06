from pyjo.exceptions import InvalidType
from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, subtype, check_elements_type=True, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=self.check_type, **kwargs)
        self.subtype = subtype
        self.check_elements_type = check_elements_type

    def check_subtype(self, value):
        if isinstance(self.subtype, Field):
            return self.subtype.check_value(value)
        else:
            return isinstance(value, self.subtype)

    def check_type(self, value):
        return isinstance(value, list) and (
                    not self.check_elements_type or all(self.check_subtype(x) for x in value))

    def patch_value(self, value):

        class TypedList(list):
            def __setitem__(_self, item_key, item_value):
                if not self.check_subtype(value):
                    raise InvalidType(attr_name=self.attr_name, type=self.check_subtype, value=item_value)
                return super(TypedList, _self).__setitem__(item_key, item_value)

        if self.check_elements_type and hasattr(value, '__setitem__'):
            value = TypedList(value)

        return value

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
            if hasattr(self.subtype, 'from_pyjson'):
                x = self.subtype.from_pyjson(x)
            res.append(x)
        return res