# Libraries


Related issues:


## Libraries as described in the RAML spec

* used to combine any collection of Data Types, Resource Types, Traits, and Security Schemes
* primarily meant to be used with external documents, but also may be defined inline

## Broad Implementation TODOs

* no need to parse objects defined in a library differently, e.g. Data Types, Resource Types, etc
* handle `uses` in the API root
* when applied, parse object references (see [Proposed API Behavior](#proposed-api-behavior) for an example/further understanding)
* If a library refers to another library, if I understand the spec correctly, it should inherit/combine

## Validation considerations

* External RAML files specifically for a library should have `#%RAML 1.0 Library`
* Valid properties for defining a library (all of which are optional):
    * `types`
    * `schemas`
    * `resourceTypes`
    * `traits`
    * `securitySchemes`
    * `annotationTypes`
    * `(<annotationName>)`
    * `uses`

## Where to start

These are educated suggestions, and more meant for developers unfamiliar with the `ramlfications` package and are wanting to contribute.

* I don't think a whole `Library` object necessarily needs to be define (but open to arguments and thoughts)
* Related, I'm not sure the Root Node needs a property, `uses`.
* Each object defined in a library should be parsed according to its respective object, e.g. Data Types, Resource Types, etc
* Validation should occur when a `uses` property is hit (see [validation considerations](#validation-considerations) above)
* Not sure if `ramlfications/loader.py` should be affected in any way; perhaps if we want to do anything special with the file header of `#%RAML 1.0 Library`
* Every library property (see the second point in [validation considerations](#validation-considerations)) is optional, aka should handle a `?` at the end of the property, e.g. `types?`

## Proposed API Behavior

### Input

Main RAML file, `api.raml` (snippet):

```RAML
#%RAML 1.0
title: Files API
uses:
  files: !include libraries/files.raml
resourceTypes:
  file: !include files-resource.raml
/files:
  type: file
```

Referred `files-resource.raml`:

```RAML
#%RAML 1.0 ResourceType
uses:
  files: !include libraries/files.raml
get:
  is: files.drm
  responses:
    200:
      body:
        application/json:
          type: files.file-type.File
```

Referred `libraries/files.raml`:

```RAML
#%RAML 1.0 Library
# This file is located at libraries/files.raml
usage: |
  Use to define some basic file-related constructs.
uses:
  file-type: !include libraries/file-type.raml
traits:
  drm:
    headers:
      drm-key:
resourceTypes:
  file:
    get:
      is: drm
    put:
      is: drm
```

Referred `libraries/file-type.raml`

```RAML
#%RAML 1.0 Library
# This file is located at libraries/file-type.raml
types:
  File:
    properties:
      name:
      length:
        type: integer
```

### Expected Output

I would imagine the Python objects/behavior would look as follows:

```python
>>> RAML_FILE = "api.raml"
>>> api = ramlfications.parse(RAML_FILE, version="1.0")
>>> api.title
'Files API'
>>> api.resources
[ResourceNode(method='get', path='/files')]
>>> files = api.resources[0]
>>> res_trait = files.traits[0]
>>> res_trait
TraitNode(name='drm')
>>>
>>> resp = files.responses[0]
>>> resp
Response(code='200')
>>> body = resp.body[0]
Body(mime_type='application/json')
>>> body.data_type
DataType(name='File')
>>> file_type = body.data_type
>>> file_type.family
'object'
>>> file_type.schema
# currently `body.schema` returns OrderedDicts
# but I could be convinced to do `jsonschema` objects for application/json
# and `lxml` objects for application/xml response bodies per issue #15
OrderedDict([('name', [OrderedDict([('type', 'string')])]), ('length', [OrderedDict([('type', 'integer')])]])
# I would also be open to something like this, not sure how other primative types would work:
OrderedDict([('name', [OrderedDict([('type', str)])]), ('length', [OrderedDict([('type', int)])]])

```
