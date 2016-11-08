from pyjo.fields.field import Field


class ConstField(Field):
    def __init__(self, value, **kwargs):
        """
        :type value: T
        :rtype: T
        """
        kwargs['default'] = value
        kwargs['editable'] = False
        super(ConstField, self).__init__(**kwargs)

    def __repr__(self):
        return '<{}(value={})>'.format(
            self.__class__.__name__, self.default)
