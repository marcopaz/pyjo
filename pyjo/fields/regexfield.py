import re

from pyjo.fields.field import Field


class RegexField(Field):
    def __init__(self, regex, **kwargs):
        """
        :rtype: str
        """
        def validator(x):
            return bool(re.match(regex, x))
        super(RegexField, self).__init__(type=str, validator=validator, **kwargs)