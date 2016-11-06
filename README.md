[![Build Status](https://travis-ci.org/marcopaz/pyjo.svg?branch=master)](https://travis-ci.org/marcopaz/pyjo)

# pyjo

> Python JSON Objects

Library to easily specify and (de)serialize data models in Python.

## Install

```
pip install pyjo
```

## How to use

First you need to create a specification of your models by using the `Model` class and of its attributes by using the the `Field` class:

```python
class Gender(Enum):
    female = 0
    male = 1

class Address(Model):
    city = Field(type=str)
    postal_code = Field(type=int, default=0)
    address = Field(default=None)

class User(Model):
    name = Field(type=str, repr=True)
    age = RangeField(min=18, max=120)
    #  equivalent to: Field(type=lambda x: isinstance(x, int) and 18 <= x <= 120)  
    gender = EnumField(enum=Gender, default=None)
    address = Field(type=Address)
```

By default any field is considered required and its presence will be checked during initialization. To modify this behavior, pass a `default` argument to the `Field` constructor:

```python
u = User(name='john', age=18)
# ...
# pyjo.exceptions.RequiredField: Field 'address' is required
```

When specified by means of the `type` argument, also the argument types are checked during initialization and assignment:

```python
u = User(name=123, age=18, address=Address(city='NYC'))
# ...
# pyjo.exceptions.InvalidType: The value of the field 'name' is not of type <class 'str'>, given 123
```

```python
u.address.city = 1
# ...
# pyjo.exceptions.InvalidType: The value of the field 'city' is not of type <class 'str'>, given 1
```

In order to serialize a model you need to call `to_json` (to obtain a JSON string) or `to_pyjson` (to obtain a JSON-serializable python object), depending on the format you want.

```python
u = User(name='john', age=18, address=Address(city='NYC'))

print(u.to_json(indent=4))
# {
#     "name": "john",
#     "gender": null,
#     "age": 18,
#     "address": {
#         "address": null,
#         "postal_code": 0,
#         "city": "NYC"
#     }
# }
```

To create a model starting from its JSON representation or python JSON-serializable dictionary, use `from_json` and `from_pyjson`:

```python
uu = User.from_json("""
    {
        "name": "john",
        "gender": "male",
        "age": 18,
        "address": {
            "address": null,
            "postal_code": 0,
            "city": "NYC"
        }
    }
    """)

print(uu)
# <User(name=john)>

print(uu.gender)
# Gender.male

print(uu.address.city)
# NYC
```
Note that the methods will also recreate all the nested objects, Python enums, etc.


## Documentation

### Field
The `Field` constructor has several _optional_ arguments:

* `type` specifies the type of the field. If specified, the type will be checked during initialization and assignment
* `default` specifies the default value for the field. When specified (even if specified with value `None`) the field is considered optional and won't raise an exception if not present during initialization
* `repr` boolean flag to indicate if the field/value should be shown in the Python representation of the object, when printed
* `editable` boolean flag that indicates if the field is editable after initialization (through assignment) or not. Default is `True`
* `to_pyjson`, `from_pyjson` (methods) to add ad-hoc JSON serialization/deserialization for a specific field


### Model

* `to_pyjson()`, `from_pyjson()` serialize/deserialize to/from JSON-serializable python objects 
* `to_json()`, `from_json()` shortcuts for `json.dumps(model.to_pyjson())` and `model.from_pyjson(json.loads(s))`


## Field subclasses

You can create subclasses of `Field` to handle specific types of objects. Several of them are already integrated in pyjo and more are coming (feel free to create a PR to add more):

* `ConstField` for constant fields (shortcut for `Field` with `editable=False`)
* `ListField` for fields containing a list of elements
* `RegexField` for fields containing a string that matches a given regex
* `RangeField` for fields containing a int with optional minimum/maximum value
