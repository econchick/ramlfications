# Extensions

Related issues:

## Extensions as described in the RAML spec

* meant to add or override a RAML API definition
* meant to address situations where an extended API functionality is given to certain clients/users (e.g. beta testing, premium clients, etc), and/or instance-specific properties (e.g. a different service endpoint/URL)
* the tree of nodes in the merged document is compared with the tree of nodes in the master RAML document after resolving all `!include` tags


## Broad Implementation TODOs

* Parse similar to data types, resource types, traits, etc with own object
* Follow merge rules (TODO: detail out)
* Figure out if `ramlfications` could/should handle only one extension at a time, or otherwise how preference is given if multiple applied extensions addresses the same properties

## Validation

* File header should be `#%RAML 1.0 Extension`
* Extension file must contain `masterRef` property

## Where to start

* Create either a method on the `RootNode` object itself (located in `ramlfications/raml.py`, or a function, AND/OR supply the extension files during `ramlfications.parse`. This functionality would actually add/apply the changes/transformation to the original API. See [proposed-api-behavior](#proposed-api-behavior) for ideas behavior.
* If chosing a separate function for the application of an extension, a helper function should placed in `ramlfications/__init__.py`, with actual function logic probably in new module where all merge rules are applied - should probably leverage the same module with Overlays.
* Note that these extensions aren't referred to by an `!include` tag. Therefore, when applying an extension, another call to the `load` function is (probably) needed.
* Process validation as defined [above](#validation)

## Proposed API behavior

### Input

Main RAML file, `api.raml` (snippet):

```RAML
#%RAML 1.0
title: Book Library API
documentation:
  - title: Introduction
    content: Automated access to books
  - title: Licensing
    content: Please respect copyrights on our books.
/books:
  description: The collection of library books
  get:
```

First extension example, `api_admin.raml`:

```RAML
#%RAML 1.0 Extension
usage: Add administrative functionality
masterRef: librarybooks.raml
/books:
  post:
    description: Add a new book to the collection
```

Second extension example, `api_piedmont.raml`:

```RAML
#%RAML 1.0 Extension
usage: The location of the public instance of the Piedmont library API
masterRef: librarybooks.raml
baseUri: http://api.piedmont-library.com
```


### Expected Output

I would imagine the Python objects/behavior would look as follows:

```python
>>> RAML_FILE = "api.raml"
>>> EXT_ADMIN = "api_admin.raml"
>>> EXT_PIEDMONT = "api_piedmont.raml"
# potential approaches to apply an extension:
#
# only one extension at a time
>>> api = ramlfications.parse(RAML_FILE, version="1.0", ext=EXT_ADMIN)
# process multiple extensions but return one API; I'm guessing order matters
>>> api = ramlfications.parse(RAML_FILE, version="1.0", exts=[EXT_ADMIN, EXT_PIEDMONT])
# process multiple extensions, and return a separate API object for each one
>>> api1, api2 = ramlfications.parse(RAML_FILE, version="1.0", exts=[EXT_ADMIN, EXT_PIEDMONT])
#
# The following would limit to one API object, may want to support both functionalities of
# processing an API during object creation as well as applying changes to an alread-created
# API object
#
# add an extension via a method on the api object, perhaps multiple times:
>>> api.extend(ext=EXT_ADMIN)
>>> api.extend(ext=EXT_PIEDMONT)
# or via a list
>>> api.extend(exts=[EXT_ADMIN, EXT_PIEDMONT])
# or a function
>>> extend(api, EXT_ADMIN)
>>> extend(api, EXT_PIEDMONT)
>>> extend(api, exts=[EXT_ADMIN, EXT_PIEDMONT])
#
# further API behavior
>>> api.base_uri
'http://api.piedmont-library.com'
>>> api.resources
[ResourceNode(method='get', path='/books'), ResourceNode(method='post', path='/books')]
```
