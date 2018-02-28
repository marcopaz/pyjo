import unittest

from pyjo import Model, Field
from pyjo.exceptions import RequiredFieldError, NotEditableField, FieldTypeError, ValidationError


class TestModel(unittest.TestCase):
    def test_required_field(self):
        class A(Model):
            foo = Field(required=True)

        with self.assertRaises(RequiredFieldError):
            a = A()

    def test_required_with_empty_default(self):
        class A(Model):
            foo = Field(type=str, required=True, default=None)

        with self.assertRaises(RequiredFieldError):
            a = A()

    def test_required_with_nonempty_default(self):
        class A(Model):
            foo = Field(type=str, required=True, default='hello')

        a = A()
        self.assertEquals(a.foo, 'hello')

    def test_required_empty_assignment(self):
        class A(Model):
            foo = Field(type=str, required=True)

        a = A(foo='bar')
        self.assertEquals(a.foo, 'bar')
        with self.assertRaises(RequiredFieldError):
            a.foo = None

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
        json = a.to_dict()
        self.assertEqual(json, {'foo': 'hello', 'bar': 123})

    def test_json_deserialization(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field()

        a = A.from_dict({'foo': 'hello', 'bar': 123})
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.bar, 123)

    def test_json_deser_without_required_fields(self):
        class A(Model):
            foo = Field(type=str, required=True)
            bar = Field(required=True)

        with self.assertRaises(RequiredFieldError):
            a = A.from_dict({'bar': 123})

    def test_json_with_submodel(self):
        class A(Model):
            foo = Field(type=str, required=True)
            bar = Field(type=int, default=0)

        class B(Model):
            submodel = Field(type=A)

        a = A(foo='foo', bar=123)
        b = B(submodel=a)

        # serialization / deserialization of the submodel
        json = b.to_dict()
        self.assertEqual(json, {'submodel': {'bar': 123, 'foo': 'foo'}})
        c = B.from_dict(json)
        self.assertEqual(c.submodel.foo, 'foo')
        self.assertEqual(c.submodel.bar, 123)

        # missing required fields of the submodel
        with self.assertRaises(RequiredFieldError):
            B.from_dict({'submodel': {'bar': 123}})

        # default values of the submodel's fields
        d = B.from_dict({'submodel': {'foo': 'foo'}})
        self.assertEqual(d.submodel.bar, 0)

    def test_multiple_nested_models(self):
        class A(Model):
            fA = Field(type=str)

        class B(Model):
            fB = Field(type=A)

        class C(Model):
            fC = Field(type=B)

        c = C(fC=B(fB=A(fA='yo')))
        pj = c.to_dict()
        self.assertEqual(pj, {'fC': {'fB': {'fA': 'yo'}}})
        c = C.from_dict(pj)
        self.assertEqual(c.fC.fB.fA, 'yo')

        with self.assertRaises(FieldTypeError):
            c = C(fC=B(fB=A(fA=1)))

    def test_discard_non_fields(self):
        class A(Model):
            foo = Field(type=str)

        a = A.from_dict({'foo': 'hello', 'foo2': 'hello2'}, discard_non_fields=False)
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(a.foo2, 'hello2')

        a = A.from_dict({'foo': 'hello', 'foo2': 'hello2'}, discard_non_fields=True)
        self.assertEqual(a.foo, 'hello')
        self.assertEqual(hasattr(a, 'foo2'), False)

    def test_model_repr(self):
        class A(Model):
            foo = Field(type=str)

        self.assertEquals(str(A(foo='bar')), '<A()>')

        class A(Model):
            foo = Field(type=str, repr=True)

        self.assertEquals(str(A(foo='bar')), '<A(foo=bar)>')

    def test_function_default(self):
        data = {'x': 0}

        def incr_x():
            data['x'] += 1
            return data['x']

        class A(Model):
            foo = Field(type=int, default=incr_x)

        self.assertEqual(A().foo, 1)
        self.assertEqual(A().foo, 2)

    def test_no_serialization_if_no_value(self):

        class A(Model):
            foo = Field(type=int)
            bar = Field(type=int, default=1)
            flag = Field(type=bool, default=False)

        a = A()
        self.assertEqual(a.to_dict(), {'bar': 1, 'flag': False})

        a.foo = 10
        self.assertEqual(a.to_dict(), {'foo': 10, 'bar': 1, 'flag': False})

        del a.foo
        del a.bar
        del a.flag
        self.assertEqual(a.to_dict(), {})

    def test_del_property(self):

        class A(Model):
            foo = Field(type=int)

        a = A()
        a.foo = 5
        self.assertEqual(a.foo, 5)
        self.assertEqual(a.to_dict()['foo'], 5)

        del a.foo
        self.assertEqual(a.foo, None)
        with self.assertRaises(KeyError):
            a.to_dict()['foo']

    def test_cast(self):
        class A(Model):
            foo = Field(type=int, cast=int)

        a = A()
        a.foo = '5'
        self.assertEqual(a.foo, 5)
        self.assertEqual(a.to_dict()['foo'], 5)
        a.foo = 5
        self.assertEqual(a.foo, 5)
        self.assertEqual(a.to_dict()['foo'], 5)
        a.foo = None
        self.assertEqual(a.foo, None)

    def test_update_from_dict(self):
        class A(Model):
            a = Field(type=str)
            b = Field(type=int, required=True)

        o = A(a='test', b=12)

        with self.assertRaises(RequiredFieldError):
            o.update_from_dict({
                'a': 'test2',
                'b': None,
            })

        with self.assertRaises(FieldTypeError):
            o.update_from_dict({
                'a': 12,
            })

        o.update_from_dict({
            'a': 'foo',
        })
        self.assertEquals(o.a, 'foo')
        self.assertEquals(o.b, 12)

        o.update_from_dict({
            'b': 1,
        })
        self.assertEquals(o.b, 1)

    def test_after_init_hook(self):
        class A(Model):
            foo = Field(type=str)
            bar = Field(type=int)

            def after_init(self):
                self.validate()

            def validate(self):
                if self.foo is None and self.bar is None:
                    raise ValidationError('one between foo and bar must be set')

        a = A(foo='hello', bar=1)
        a = A(foo='hello')
        a = A(bar=1)

        with self.assertRaises(ValidationError):
            a = A()


if __name__ == '__main__':
    unittest.main()
