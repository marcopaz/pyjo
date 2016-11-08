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
                raise ValidationError('value does not match regex'.format())

        try:
            basestr_t = basestring
        except NameError:
            basestr_t = str

        super(RegexField, self).__init__(type=basestr_t, validator=validator, **kwargs)
