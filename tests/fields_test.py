import unittest

from pyjo import Model, Field, ConstField, EnumField, RangeField, RegexField, ListField
from pyjo.exceptions import RequiredField, NotEditableField, InvalidType
from enum import Enum


class FieldsModel(unittest.TestCase):

    def test_enum_field(self):

        class MyEnum(Enum):
            foo1 = 1
            foo2 = 2

        class A(Model):
            foo = EnumField(MyEnum)

        a = A(foo=MyEnum.foo1)
        self.assertEqual(a.to_pyjson()['foo'], 'foo1')

        with self.assertRaises(InvalidType):
            a.foo = 'foo2'

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
            a.foo = ['foo']

    def test_const_field(self):

        class A(Model):
            foo = ConstField('hello')

        a = A()
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.to_pyjson()['foo'], 'hello')

        with self.assertRaises(NotEditableField):
            a.foo = 'olleh'

    def test_range_field(self):

        class A(Model):
            foo = RangeField(min=18, max=80)

        with self.assertRaises(RequiredField):
            A()

        a = A(foo=20)
        self.assertEqual(a.foo, 20)
        self.assertEqual(a.to_pyjson()['foo'], 20)

        with self.assertRaises(InvalidType):
            a.foo = 17

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