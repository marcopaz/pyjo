import unittest

from pyjo import Model, Field, ListField
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

        self.assertEqual(a.to_dict(), {'foo': [{'n': 1}, {'n': 2}, {'n': 3}]})
        aa = A.from_dict({'foo': [{'n': 1}, {'n': 2}, {'n': 3}]})
        self.assertEqual(len(aa.foo), 3)
        self.assertEqual(aa.foo[1].n, 2)

    def test_list_serialization(self):

        class A(Model):
            foo = ListField(str)

        a = A(foo=['foo1', 'foo2', 'foo3'])
        self.assertEqual(len(a.foo), 3)
        self.assertEqual(a.foo[0], 'foo1')
        self.assertEqual(a.foo[1], 'foo2')
        self.assertEqual(a.foo[2], 'foo3')

        self.assertEqual(a.to_dict(), {'foo': ['foo1', 'foo2', 'foo3']})
        aa = A.from_dict({'foo': ['foo1', 'foo2', 'foo3']})
        self.assertEqual(len(aa.foo), 3)
        self.assertEqual(aa.foo[1], 'foo2')

        a.foo = ['foo1']
        self.assertEqual(len(a.foo), 1)
        # with self.assertRaises(ValidationError):
        #     a.foo[0] = 'bar'

    def test_list_with_validator(self):
        import re

        def validator(values):
            for i, x in enumerate(values):
                if not isinstance(x, str) or not re.match('foo[0-9]', x):
                    raise ValidationError('element at index {} does not match the regex'.format(i))

        class A(Model):
            foo = ListField(str, validator=validator)

        a = A(foo=['foo1', 'foo2', 'foo3'])

        with self.assertRaises(ValidationError):
            a = A(foo=['foo1', 2, 'foo3'])

        with self.assertRaises(FieldTypeError):
            a.foo = 'hello'

        # NOT IMPLEMENTED
        # with self.assertRaises(FieldTypeError):
        #     a.foo[1] = 1


if __name__ == '__main__':
    unittest.main()
