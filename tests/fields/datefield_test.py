import unittest
from datetime import datetime

from pyjo import Model, DatetimeField
from pyjo.exceptions import FieldTypeError


class DatetimeFieldTest(unittest.TestCase):

    def test_datetimefield(self):

        class A(Model):
            date = DatetimeField()

        time = 1478390400
        dt = datetime.utcfromtimestamp(time)

        a = A(date=dt)
        self.assertEqual(a.date, dt)

        with self.assertRaises(FieldTypeError):
            a.date = 'hello'

        pj = a.to_dict()
        self.assertEqual(pj['date'], time)
        aa = A.from_json(a.to_json())
        self.assertEqual(aa.date, dt)


if __name__ == '__main__':
    unittest.main()
