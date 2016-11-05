import unittest

from pyjo import Model, Field, ConstField
from pyjo.exceptions import RequiredField, NotEditableField, InvalidType


class TestModel(unittest.TestCase):

    def test_required_field(self):
        class A(Model):
            foo = Field()
        with self.assertRaises(RequiredField):
            a = A()

    def test_default_value(self):
        class A(Model):
            foo = Field(default='foo')
        a = A()
        self.assertEqual(a.foo, 'foo')

    def test_constant_field(self):
        class A(Model):
            foo = ConstField('foo')
        a = A()
        self.assertEqual(a.foo, 'foo')
        with self.assertRaises(NotEditableField):
            a.foo = 'bar'

    def test_invalid_type_on_init(self):
        class A(Model):
            foo = Field(type=str)
        with self.assertRaises(InvalidType):
            a = A(foo=1)

    def test_invalid_type_on_set(self):
        class A(Model):
            foo = Field(type=str)
        a = A(foo='foo')
        self.assertEqual(a.foo, 'foo')
        with self.assertRaises(InvalidType):
            a.foo = 123

    def test_function_type(self):
        class A(Model):
            foo = Field(type=lambda x: isinstance(x, str) and x.startswith('#'))
        with self.assertRaises(InvalidType):
            a = A(foo=1)
        with self.assertRaises(InvalidType):
            a = A(foo='hello')
        a = A(foo='#hello')
        self.assertEqual(a.foo, '#hello')

    def test_json_serialization(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field(type=int)
        a = A(foo='hello', bar=123)
        json = a.to_json()
        self.assertEqual(json , {'foo': 'hello', 'bar': 123})

    def test_json_deserialization(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field()
        a = A.from_json({'foo': 'hello', 'bar': 123})
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.bar, 123)

    def test_json_deser_without_required_fields(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field()
        with self.assertRaises(RequiredField):
            a = A.from_json({'bar': 123})


if __name__ == '__main__':
    unittest.main()