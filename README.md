[![Build Status](https://travis-ci.org/marcopaz/pyjo.svg?branch=master)](https://travis-ci.org/marcopaz/pyjo)

# pyjo

> Python JSON Objects

Easily specify and (de)serialize data models in Python.

## Install

```
pip install pyjo
```

## How to use

First you need to create a specification of your models and attributes by using the `Model` and the `Field` classes:

```python
from pyjo import Model, Field, RangeField, EnumField

class Gender(Enum):
    female = 0
    male = 1

class Address(Model):
    city = Field(type=str)
    postal_code = Field(type=int)
    address = Field()

class User(Model):
    name = Field(type=str, repr=True, required=True)
    age = RangeField(min=18, max=120)
    #  equivalent to: Field(type=int, validator=lambda x: 18 <= x <= 120)
    gender = EnumField(enum=Gender)
    address = Field(type=Address)
```

By default any field is considered optional unless specified with `required` attribute. If required, its presence will be checked during initialization.

```python
u = User()
# ...
# pyjo.exceptions.RequiredField: Field 'name' is required
```

```python
User(name='john', age=18, address=Address(city='NYC'))
# <User(name=john)>
```

When the `type` argument is provided, the type of the value assigned to a field will be checked during initialization and assignment:

```python
User(name=123)
# ...
# pyjo.exceptions.InvalidType: The value of the field 'name' is not of type str, given 123
```

```python
u.address.city = 1
# ...
# pyjo.exceptions.InvalidType: The value of the field 'city' is not of type str, given 1
```

In order to serialize a model you need to call `to_dict`:

```python
u = User(name='john', age=18, address=Address(city='NYC'))

print(u.to_dict())
# {
#     "name": "john",
#     "age": 18,
#     "address": {
#         "city": "NYC"
#     }
# }
```

To create a model starting from its python dictionary representation, use `from_dict`:

```python
u = User.from_dict({
        "name": "john",
        "gender": "male",
        "age": 18,
        "address": {
            "city": "NYC"
        }
    })

print(u)
# <User(name=john)>

print(u.gender)
# Gender.male

print(u.address.city)
# NYC
```
Note that `from_dict` will also recreate all the nested pyjo objects.


# API Documentation

## Field
The `Field` object has several _optional_ arguments:

* `type` specifies the type of the field. If specified, the type will be checked during initialization and assignment
* `default` specifies the default value for the field. The value of a default can be a function and it will be computed and assigned during the initialization of the object
* `required` boolean flag to indicate if the field must be specified and can't be `None`, even during assignment (`False` by default)
* `repr` boolean flag to indicate if the field/value should be shown in the Python representation of the object, when printed (`False` by default)
* `to_dict`, `from_dict` (functions) to add ad-hoc serialization/deserialization for the field
* `validator` (function) function that gets called to validate the input (after cast) of a field
* `cast` (function) cast value of the field (if not empty) before (validation and) assignment

## Model

* `to_dict()`, `from_dict()` serialize/deserialize to/from python dictionaries
* `to_json()`, `from_json()` shortcuts for `json.dumps(model.to_dict())` and `Model.from_dict(json.loads(<dict>))`

## Field subclasses

You can easily create subclasses of `Field` to handle specific types of objects. Several of them are already integrated in pyjo and more are coming (feel free to create a PR to add more):

* `ListField` for fields containing a list of elements
* `RegexField` for fields containing a string that matches a given regex
* `RangeField` for fields containing a int with optional minimum/maximum value
* `DatetimeField` for fields containing a UTC datetime

# Extensions

* [pyjo_mongo](https://github.com/marcopaz/pyjo_mongo) easily interact with MongoDB documents, a lightweight replacement of the `mongoengine` library
