import unittest

from pyjo import Model, ConstField
from pyjo.exceptions import NotEditableField


class ConstFieldTest(unittest.TestCase):

    def test_const_field(self):

        class A(Model):
            foo = ConstField('hello')

        a = A()
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.to_pyjson()['foo'], 'hello')

        with self.assertRaises(NotEditableField):
            a.foo = 'olleh'


if __name__ == '__main__':
    unittest.main()
