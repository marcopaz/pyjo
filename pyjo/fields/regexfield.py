import re

from pyjo.fields.field import Field


class RegexField(Field):
    def __init__(self, regex, **kwargs):
        """
        :rtype: str
        """
        def type_(x):
            return isinstance(x, str) and re.match(regex, x)
        super(RegexField, self).__init__(type=type_, **kwargs)