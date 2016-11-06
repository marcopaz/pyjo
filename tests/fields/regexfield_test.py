import unittest

from pyjo import Model, RegexField
from pyjo.exceptions import RequiredField, InvalidType


class RegexFieldTest(unittest.TestCase):

    def test_regex_field(self):

        class A(Model):
            foo = RegexField('foo[0-9]')

        with self.assertRaises(RequiredField):
            A()

        a = A(foo='foo1')
        self.assertEqual(a.foo, 'foo1')
        self.assertEqual(a.to_pyjson()['foo'], 'foo1')

        with self.assertRaises(InvalidType):
            a.foo = 'bar1'


if __name__ == '__main__':
    unittest.main()
