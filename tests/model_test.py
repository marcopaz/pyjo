import unittest

from pyjo import Model, Field
from pyjo.exceptions import RequiredFieldError, NotEditableField, FieldTypeError, ValidationError


class TestModel(unittest.TestCase):

    def test_required_field(self):
        class A(Model):
            foo = Field()
        with self.assertRaises(RequiredFieldError):
            a = A()

    def test_default_value(self):
        class A(Model):
            foo = Field(default='foo')
        a = A()
        self.assertEqual(a.foo, 'foo')

    def test_default_value_invalid_type(self):
        class A(Model):
            foo = Field(default='foo', type=int)

        with self.assertRaises(FieldTypeError):
            a = A()

    def test_type_empty_default(self):
        class A(Model):
            foo = Field(type=str, default=None)
        a = A()
        a.foo = 'hello'
        self.assertEqual(a.foo, 'hello')

    def test_editable_field(self):
        class A(Model):
            foo = Field(default='foo', editable=True)
        a = A(foo=123)
        self.assertEqual(a.foo, 123)
        a.foo = 321
        self.assertEqual(a.foo, 321)

    def test_not_editable_field(self):
        class A(Model):
            foo = Field(editable=False)

        a = A(foo=123)
        self.assertEqual(a.foo, 123)

        with self.assertRaises(NotEditableField):
            a.foo = 321

    def test_invalid_type_on_init(self):
        class A(Model):
            foo = Field(type=str)
        with self.assertRaises(FieldTypeError):
            a = A(foo=1)

    def test_invalid_type_on_set(self):
        class A(Model):
            foo = Field(type=str)
        a = A(foo='foo')
        self.assertEqual(a.foo, 'foo')
        with self.assertRaises(FieldTypeError):
            a.foo = 123

    def test_validator(self):
        class A(Model):
            foo = Field(type=str, validator=lambda x: x.startswith('#'))
        with self.assertRaises(FieldTypeError):
            a = A(foo=1)
        with self.assertRaises(ValidationError):
            a = A(foo='hello')
        a = A(foo='#hello')
        self.assertEqual(a.foo, '#hello')

    def test_json_serialization(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field(type=int)
        a = A(foo='hello', bar=123)
        json = a.to_pyjson()
        self.assertEqual(json , {'foo': 'hello', 'bar': 123})

    def test_json_deserialization(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field()
        a = A.from_pyjson({'foo': 'hello', 'bar': 123})
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.bar, 123)

    def test_json_deser_without_required_fields(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field()
        with self.assertRaises(RequiredFieldError):
            a = A.from_pyjson({'bar': 123})

    def test_json_with_submodel(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field(type=int, default=0)

        class B(Model):
            submodel = Field(type=A)

        a = A(foo='foo', bar=123)
        b = B(submodel=a)

        # serialization / deserialization of the submodel
        json = b.to_pyjson()
        self.assertEqual(json, {'submodel': {'bar': 123, 'foo': 'foo'}})
        c = B.from_pyjson(json)
        self.assertEqual(c.submodel.foo, 'foo')
        self.assertEqual(c.submodel.bar, 123)

        # missing required fields of the submodel
        with self.assertRaises(RequiredFieldError):
            B.from_pyjson({'submodel': {'bar': 123}})

        # default values of the submodel's fields
        d = B.from_pyjson({'submodel': {'foo': 'foo'}})
        self.assertEqual(d.submodel.bar, 0)

    def test_multiple_nested_models(self):
        class A(Model):
            fA = Field(type=str)
        class B(Model):
            fB = Field(type=A)
        class C(Model):
            fC = Field(type=B)

        c = C(fC=B(fB=A(fA='yo')))
        pj = c.to_pyjson()
        self.assertEqual(pj, {'fC': {'fB': {'fA': 'yo'}}})
        c = C.from_pyjson(pj)
        self.assertEqual(c.fC.fB.fA, 'yo')

        with self.assertRaises(FieldTypeError):
            c = C(fC=B(fB=A(fA=1)))

    def test_discard_non_fields(self):

        class A(Model):
            foo = Field(type=str)

        a = A.from_pyjson({'foo': 'hello', 'foo2': 'hello2'}, discard_non_fields=False)
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.foo2, 'hello2')

        a = A.from_pyjson({'foo': 'hello', 'foo2': 'hello2'}, discard_non_fields=True)
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(hasattr(a, 'foo2'), False)

    def test_model_repr(self):
        class A(Model):
            foo = Field(type=str)

        self.assertEquals(str(A(foo='bar')), '<A()>')

        class A(Model):
            foo = Field(type=str, repr=True)

        self.assertEquals(str(A(foo='bar')), '<A(foo=bar)>')
if __name__ == '__main__':
    unittest.main()