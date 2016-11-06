import unittest

from pyjo import Model, Field, ListField, RegexField
from pyjo.exceptions import FieldTypeError, ValidationError


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
        with self.assertRaises(ValidationError):
            a.foo = ['bar']
        with self.assertRaises(ValidationError):
            a.foo[0] = 'bar'

    def test_list_with_subtype(self):

        class A(Model):
            foo = ListField(str)

        a = A(foo=['foo1', 'foo2', 'foo3'])

        with self.assertRaises(FieldTypeError):
            a = A(foo=['foo1', 2, 'foo3'])

        with self.assertRaises(FieldTypeError):
            a.foo = 'olleh'

        with self.assertRaises(FieldTypeError):
            a.foo[1] = 1

    def test_nested_lists_errors(self):

        class A(Model):
            foo = ListField(ListField(int))

        try:
            a = A(foo=[['foo']])
        except FieldTypeError as e:
            self.assertEqual(e.message, 'A.foo[0][0] is not of type int')

        class A(Model):
            foo = ListField(ListField(RegexField('[a-c][0-9]')))

        try:
            a = A(foo=[['a0', 'yo']])
        except ValidationError as e:
            self.assertEqual(e.message, 'A.foo[0][1] did not pass the validation: value did not match regex')


if __name__ == '__main__':
    unittest.main()
