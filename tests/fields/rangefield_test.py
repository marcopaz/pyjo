import unittest

from pyjo import Model, RangeField
from pyjo.exceptions import RequiredFieldError, ValidationError


class RangeFieldTest(unittest.TestCase):

    def test_range_field(self):

        class A(Model):
            foo = RangeField(min=18, max=80, required=True)

        with self.assertRaises(RequiredFieldError):
            A()

        a = A(foo=20)
        self.assertEqual(a.foo, 20)
        self.assertEqual(a.to_dict()['foo'], 20)

        with self.assertRaises(ValidationError):
            a.foo = 17


if __name__ == '__main__':
    unittest.main()
