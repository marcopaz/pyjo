from pyjo.exceptions import TypeError, ValidationError
from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, subtype, check_elements_type=True, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=list, validator=self._check_subtypes, **kwargs)
        self._subtype = subtype
        self._check_elements_type = check_elements_type

    def _check_subtype(self, value):
        if isinstance(self._subtype, Field):
            try:
                self._subtype.check_value(value)
            except (TypeError, ValidationError):
                return False
            return True
        else:
            return isinstance(value, self._subtype)

    def _check_subtypes(self, value):
        return not self._check_elements_type or all(self._check_subtype(x) for x in value)

    def _patch_value(self, value):

        class TypedList(list):
            def __setitem__(_self, item_key, item_value):
                if not self._check_subtype(value):
                    raise TypeError(attr_name=self._attr_name, type=self._check_subtype, value=item_value)
                return super(TypedList, _self).__setitem__(item_key, item_value)

        if self._check_elements_type and hasattr(value, '__setitem__'):
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
            if hasattr(self._subtype, 'from_pyjson'):
                x = self._subtype.from_pyjson(x)
            res.append(x)
        return res