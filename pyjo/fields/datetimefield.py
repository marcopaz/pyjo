from datetime import datetime

from pyjo.fields.field import Field


def dt_to_timestamp(dt):
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None) - dt.utcoffset()
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    return int(timestamp)


class DatetimeField(Field):
    def __init__(self, **kwargs):
        """
        :rtype: datetime
        """
        super(DatetimeField, self).__init__(type=datetime, **kwargs)

    def from_dict(self, value):
        if value is None:
            return value
        return datetime.utcfromtimestamp(int(value))

    def to_dict(self, value):
        if value is None:
            return value
        return dt_to_timestamp(value)

