from pyjo.exceptions import FieldTypeError, ValidationError
from pyjo.fields.field import Field


class ListField(Field):
    def __init__(self, subtype=None, check_elements_type=True, **kwargs):
        """
        :type model: T
        :rtype: list[T]
        """
        super(ListField, self).__init__(type=list, validator=self._check_subtypes, **kwargs)
        self._subtype = subtype or object
        self._check_elements_type = check_elements_type if subtype is not None else False

    def _check_subtypes(self, value):
        if not self._check_elements_type:
            return
        for i, x in enumerate(value):
            self._check_subtype(i, x)

    def _check_subtype(self, index, value):
        if isinstance(self._subtype, Field):
            self._subtype._attr_name = '{}[{}]'.format(self._attr_name, index)
            self._subtype.check_value(value)
        elif not isinstance(value, self._subtype):
            raise FieldTypeError('{}[{}] is not of type {}'.format(self._attr_name, index, self._subtype.__name__))

    def _patch_value(self, value):

        class TypedList(list):
            def __setitem__(_self, item_key, item_value):
                self._check_subtype(item_key, item_value)
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