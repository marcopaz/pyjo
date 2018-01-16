import unittest

from pyjo import Model, RegexField
from pyjo.exceptions import RequiredFieldError, ValidationError


class RegexFieldTest(unittest.TestCase):

    def test_regex_field(self):

        class A(Model):
            foo = RegexField('foo[0-9]', required=True)

        with self.assertRaises(RequiredFieldError):
            A()

        a = A(foo='foo1')
        self.assertEqual(a.foo, 'foo1')
        self.assertEqual(a.to_dict()['foo'], 'foo1')

        with self.assertRaises(ValidationError):
            a.foo = 'bar1'

    def test_unicode(self):

        class A(Model):
            foo = RegexField('foo[0-9]')

        a = A(foo=u'foo1')
        self.assertEquals(a.foo, u'foo1')

if __name__ == '__main__':
    unittest.main()
