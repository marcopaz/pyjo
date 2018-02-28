from __future__ import unicode_literals
from builtins import str
import unittest
from datetime import datetime

from pyjo import Model, DatetimeField
from pyjo.exceptions import FieldTypeError, RequiredFieldError
from pyjo.fields.field import Field
from pyjo.fields.mapfield import MapField


class MapFieldTest(unittest.TestCase):
    def test_map_of_datetimefield(self):
        class A(Model):
            dates = MapField(inner_field=DatetimeField())

        time = 1478390400
        dt = datetime.utcfromtimestamp(time)

        a = A(dates={'one': dt})
        self.assertEqual(a.dates['one'], dt)

        with self.assertRaises(FieldTypeError):
            a.dates = 'hello'

        pj = a.to_dict()
        self.assertEqual(pj['dates']['one'], time)
        aa = A.from_json(a.to_json())
        self.assertEqual(aa.dates['one'], dt)

    def test_map_of_str(self):
        class B(Model):
            data = MapField(inner_field=Field(type=str))

        a = B(data={'one': 'banana'})
        self.assertEqual(a.data['one'], 'banana')

        pj = a.to_dict()
        self.assertEqual(pj['data']['one'], 'banana')
        aa = B.from_json(a.to_json())
        self.assertEqual(aa.data['one'], 'banana')

    def test_map_of_int(self):
        class B(Model):
            data = MapField(inner_field=Field(type=int))

        a = B(data={'one': 1})
        self.assertEqual(a.data['one'], 1)

        pj = a.to_dict()
        self.assertEqual(pj['data']['one'], 1)
        aa = B.from_json(a.to_json())
        self.assertEqual(aa.data['one'], 1)

    def test_map_of_embedded(self):
        class A(Model):
            a = Field(type=int)
            b = Field(type=str)

        class B(Model):
            data = MapField(inner_field=Field(type=A))

        a = B(data={
            'one': A(a=1, b='one'),
            'two': A(a=2, b='two'),
        })

        self.assertEqual(a.data['one'].a, 1)
        self.assertEqual(a.data['one'].b, 'one')

        self.assertEqual(a.data['two'].a, 2)
        self.assertEqual(a.data['two'].b, 'two')

        pj = a.to_dict()
        self.assertEqual(pj['data']['one']['a'], 1)
        self.assertEqual(pj['data']['two']['a'], 2)

        aa = B.from_json(a.to_json())
        self.assertEqual(aa.data['one'].a, 1)
        self.assertEqual(aa.data['two'].a, 2)
        self.assertEqual(aa.data['two'].b, 'two')

    def test_raises_if_validation_fails(self):
        class B(Model):
            data = MapField(inner_field=Field(type=int))

        B(data={'one': 1})
        B(data={})
        B()
        with self.assertRaises(FieldTypeError):
            B(data=1)

        with self.assertRaises(FieldTypeError):
            B(data={'one': 'string'})

        with self.assertRaises(FieldTypeError):
            B(data={'one': datetime.now()})

    def test_required_works(self):
        class B(Model):
            data = MapField(inner_field=Field(type=int), required=True)

        B(data={'one': 1})
        with self.assertRaises(RequiredFieldError):
            B()

    def test_map_with_inner_cast(self):
        class B(Model):
            data = MapField(inner_field=Field(type=int, cast=int), required=True)

        b = B(data={'one': '1'})
        assert b.data['one'] == 1

    def test_name_inner_field(self):
        class A(Model):
            foo = MapField(Field(type=int))

        a = A()
        try:
            a.foo = {'foo': 'bar'}
            raise Exception('should have raised a FieldTypeError')
        except FieldTypeError as e:
            assert 'foo inner field value is not of type' in str(e)


if __name__ == '__main__':
    unittest.main()
