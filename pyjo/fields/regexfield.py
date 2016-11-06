import re

from pyjo.exceptions import ValidationError
from pyjo.fields.field import Field


class RegexField(Field):
    def __init__(self, regex, **kwargs):
        """
        :rtype: str
        """
        def validator(x):
            if not bool(re.match(regex, x)):
                raise ValidationError('value did not match regex'.format())
        super(RegexField, self).__init__(type=str, validator=validator, **kwargs)