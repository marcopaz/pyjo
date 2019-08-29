import unittest
from enum import Enum

from pyjo import Model, EnumField
from pyjo.exceptions import FieldTypeError


class EnumFieldTest(unittest.TestCase):

    def test_enum_field(self):
        class MyEnum(Enum):
            foo1 = 1
            foo2 = 2

        class A(Model):
            foo = EnumField(MyEnum)

        a = A(foo=MyEnum.foo1)
        self.assertEqual(a.to_dict()['foo'], 'foo1')

        with self.assertRaises(FieldTypeError):
            a.foo = 'foo2'

    def test_enum_field_with_value(self):
        class MyEnum(Enum):
            foo1 = 1
            foo2 = 2

        class A(Model):
            foo = EnumField(MyEnum, use_name=False)

        a = A(foo=MyEnum.foo1)
        self.assertEqual(a.to_dict()['foo'], 1)

        with self.assertRaises(FieldTypeError):
            a.foo = 'foo2'


if __name__ == '__main__':
    unittest.main()
