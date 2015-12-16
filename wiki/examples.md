# Examples

Related issues:

## Examples as described in the RAML spec

* Sort of separate from `example` attribute that already exists; this new feature is sometimes referred to as "Named Examples"
* Applies **only** to Data Types
* `examples` property may be used to attach multiple examples
* `examples` can be an array or a map/dictionary

## Broad Implementation TODOs

* Parse similar to data types, resource types, etc with own object
* Able to handle both arrays and maps/dicts for `examples`
* `example` as defined in a Data Type will mirror the same properties as the Data Type's properties, e.g. a map of key/value pairs
* If `strict` is set to false, then validation of the primative type of the example shouldn't happen

## Validation

* Each example has the following properties; all are optional _except_ for `content`:
    * `displayName`
    * `description`
    * `(<annotationName>)`
    * `content`
    * `strict`

## Where to start

* A new `Example` object should probably be defined in `ramlfications/raml.py`
* When parsing DataTypes, the `example` and/or `examples` property should be appropriately parsed, and validated (e.g. the type of example matches the expected type defined in the property itself)
* In `ramlfications/parser.py`, there should be a function within the data type function to create these example objects
* `ramlfications/validate.py` should ensure the above [validation](#validation)
* This should probably be tackled at the same time Data Types are tackled.

## Proposed API behavior

### Input

Main RAML file, `api.raml`:

```RAML
#%RAML 1.0
title: API with Examples
types:
  User:
    type: object
    properties:
      name: string
      lastname: string
    example:
      name: Bob
      lastname: Marley
  Org:
    type: object
    properties:
      name: string
      address?: string
    examples:
      - content:
          name: Acme
      - content:
          name: Software Corp
          address: 35 Central Street
  Org_alt:
    type: object
    properties:
      name: string
      address?: string
    examples:
      acme:
        content:
          name: Acme
      softwareCorp:
        content:
          name: Software Corp
          address: 35 Central Street
```

### Expected output

```python
>>> RAML_FILE = "api.raml"
>>> api = ramlfications.parse(RAML_FILE, version="1.0")
>>> api.title
'API with Examples'
>>> user = api.data_types[0]
>>> user
DataType(name='User')
>>> user.examples # not set so nothing returns
>>> user.example
Example(of='User')
>>> dir(user.example)  # skipping dunders
['name',
'lastname',
'type']
>>> user.example.name
'Bob'
>>> user.example.lastname
'Marley'
>>> user.example.type
str # or 'string'
>>> org = api.data_types[1]
>>> org.example # not set so nothing returns
>>> org.examples
[Example(of='Org'), Example(of='Org')]  # not sure how to diff these two
>>> org.examples[0].name
'Acme'
>>> org.examples[1].name
'Software Corp'
>>> org.examples[1].address
'35 Central Street'
>>> org_alt = api.data_types[2]
>>> org_alt.examples
[Example(of='acme'), Example(of='softwareCorp')]
>>> org_alt.examples[0].name
'Acme'
>>> org_alt.examples[1].name
'Software Corp'
>>> org_alt.examples[1].address
'35 Central Street'
```
