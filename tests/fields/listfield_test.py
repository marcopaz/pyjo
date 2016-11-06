import unittest

from pyjo import Model, Field, ListField, RegexField
from pyjo.exceptions import InvalidType


class ListFieldTest(unittest.TestCase):

    def test_model_list_field(self):
        class B(Model):
            n = Field(type=int)

        class A(Model):
            foo = ListField(B)

        a = A(foo=[B(n=1), B(n=2), B(n=3)])
        self.assertEqual(len(a.foo), 3)
        self.assertEqual(a.foo[0].n, 1)
        self.assertEqual(a.foo[1].n, 2)
        self.assertEqual(a.foo[2].n, 3)

        self.assertEqual(a.to_pyjson(), {'foo': [{'n': 1}, {'n': 2}, {'n': 3}]})
        aa = A.from_pyjson({'foo': [{'n': 1}, {'n': 2}, {'n': 3}]})
        self.assertEqual(len(aa.foo), 3)
        self.assertEqual(aa.foo[1].n, 2)

    def test_list_of_fields(self):

        class A(Model):
            foo = ListField(RegexField('foo[0-9]'))

        a = A(foo=['foo1', 'foo2', 'foo3'])
        self.assertEqual(len(a.foo), 3)
        self.assertEqual(a.foo[0], 'foo1')
        self.assertEqual(a.foo[1], 'foo2')
        self.assertEqual(a.foo[2], 'foo3')

        self.assertEqual(a.to_pyjson(), {'foo': ['foo1', 'foo2', 'foo3']})
        aa = A.from_pyjson({'foo': ['foo1', 'foo2', 'foo3']})
        self.assertEqual(len(aa.foo), 3)
        self.assertEqual(aa.foo[1], 'foo2')

        a.foo = ['foo1']
        self.assertEqual(len(a.foo), 1)
        with self.assertRaises(InvalidType):
            a.foo = ['bar']
        with self.assertRaises(InvalidType):
            a.foo[0] = 'bar'

    def test_list_with_subtype(self):

        class A(Model):
            foo = ListField(str)

        a = A(foo=['foo1', 'foo2', 'foo3'])

        with self.assertRaises(InvalidType):
            a = A(foo=['foo1', 2, 'foo3'])

        with self.assertRaises(InvalidType):
            a.foo = 'olleh'

        with self.assertRaises(InvalidType):
            a.foo[1] = 'olleh'


if __name__ == '__main__':
    unittest.main()
