import unittest

from pyjo import Model, Field, ListField
from pyjo.exceptions import FieldTypeError, ValidationError


class ListFieldTest(unittest.TestCase):

    def test_model_list_field(self):
        class B(Model):
            n = Field(type=int)

        class A(Model):
            foo = ListField(Field(type=B))

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
            foo = ListField(Field(type=str))

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
            foo = ListField(Field(type=str), validator=validator)

        a = A(foo=['foo1', 'foo2', 'foo3'])

        with self.assertRaises(ValidationError):
            a = A(foo=['foo1', 2, 'foo3'])

        with self.assertRaises(FieldTypeError):
            a.foo = 'hello'

        # NOT IMPLEMENTED
        # with self.assertRaises(FieldTypeError):
        #     a.foo[1] = 1

    def test_list_with_cast(self):
        class A(Model):
            foo = ListField(Field(type=int, cast=int), cast=lambda x: x.split(',') if isinstance(x, str) else x)

        a = A(foo="1,2,5")
        assert a.foo[0] == 1
        assert a.foo[1] == 2
        assert a.foo[2] == 5

    def test_name_inner_field(self):
        class A(Model):
            foo = ListField(Field(type=int))

        a = A()
        try:
            a.foo = ['asd']
            raise Exception('should have raised a FieldTypeError')
        except FieldTypeError as e:
            assert 'foo inner field value is not of type' in str(e)


if __name__ == '__main__':
    unittest.main()
