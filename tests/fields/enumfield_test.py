import unittest
from enum import Enum

from pyjo import Model, EnumField
from pyjo.exceptions import InvalidType


class EnumFieldTest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
