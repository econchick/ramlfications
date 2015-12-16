# Overlays

Related issues:

## Overlays as described in the RAML spec

* meant to add or override a RAML API definition
* Only certain properties can be overlayed, e.g. documentation, annotations
* Properties like resources, methods, parameters, etc, can *not* be overlayed
* meant to address problems like localization of documentation, implementation & verification information for the use of automated tools
* the tree of nodes in the merged document is compared with the tree of nodes in the master RAML document after resolving all `!include` tags

## Broad Implementation TODOs

* Parse similar to data types, resource types, traits, etc with own object
* Follow merge rules (TODO: detail out)
* Figure out if `ramlfications` could/should handle only one overlay at a time, or otherwise how preference is given if multiple applied overlays addresses the same properties

## Validation

* File header should be `#%RAML 1.0 Overlay`
* Overlay file must contain `masterRef` property
* Only allow the following differences (taken directly from the spec):


| Property             |  Allowed Differences                          |
|----------------------|-----------------------------------------------|
| title, description, documentation, displayName, usage, example | The merged tree may include new properties of this type, or properties with different values than those in the master tree   |
| types      | In addition to allowed differences described elsewhere in this table, the merged tree may also include new data types. |
| annotationTypes | The merged tree may include new annotation types, or new values for existing annotation types, as long as all annotations in the merged API definition validate against the annotation types in the merged tree. |
| any annotation property | The merged tree may include new annotations of annotation types declared in the merged tree, or annotations with different values than those in the master tree |
| named examples | The merged tree may contain new named examples, or named examples with different values than those in the master tree |
| documentation items | The merged tree may contain new items in the array that is the value of the documentation root-level property. To change or remove existing items, the documentation property itself may be overridden in the overlay. |


## Where to start

* Create either a method on the `RootNode` object itself (located in `ramlfications/raml.py`, or a function, AND/OR supply the overlay files during `ramlfications.parse`. This functionality would actually apply the changes/transformation to the original API. See [proposed-api-behavior](#proposed-api-behavior) for ideas behavior.
* If chosing a separate function for the application of an overlay, a helper function should placed in `ramlfications/__init__.py`, with actual function logic probably in new module where all merge rules are applied
* Note that these overlays aren't referred to by an `!include` tag. Therefore, when applying an overlay, another call to the `load` function is (probably) needed.
* Process validation as defined [above](#validation)

## Proposed API behavior

### Input

Main RMAL file, `api.raml` (snippet):

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

First overlay example, `api_es.raml`:

```RAML
#%RAML 1.0 Overlay
usage: Spanish localization
masterRef: librarybooks.raml
documentation:
  - title: Introducción
    content: El acceso automatizado a los libros
  - title: Licencias
    content: Por favor respeta los derechos de autor de los libros
/books:
  description: La colección de libros de la biblioteca
```

Second overlay example, `api_monitoring.raml`:

```RAML
#%RAML 1.0 Overlay
usage: Hints for monitoring the library books API
masterRef: librarybooks.raml
annotationTypes:
  monitor:
    parameters:
      frequency:
        properties:
          interval: integer
          unitOfMeasure:
            enum: [ seconds, minutes, hours ]
      script:
/books:
  get:
    (monitor):
      frequency:
        interval: 5
        unitOfMeasure: minutes
      script: randomBooksFetch
```

### Expected Output

I would imagine the Python objects/behavior would look as follows:

```python
>>> RAML_FILE = "api.raml"
>>> OVERLAY_ES = "api_es.raml"
>>> OVERLAY_MONITOR = "api_monitoring.raml"
# potential approaches to apply an overlay:
#
# only one overlay at a time
>>> api = ramlfications.parse(RAML_FILE, version="1.0", overlay=OVERLAY_ES)
# process multiple overlays but return one API, order matters
>>> api = ramlfications.parse(RAML_FILE, version="1.0", overlays=[OVERLAY_ES, OVERLAY_MONITOR])
# process multiple overlays, and return a separate API object for each one
>>> api1, api2 = ramlfications.parse(RAML_FILE, version="1.0", overlays=[OVERLAY_ES, OVERLAY_MONITOR])
#
# The following would limit to one API object, may want to support both functionalities of
# processing an API during object creation as well as applying changes to an alread-created
# API object
#
# apply an overlay via a method on the api object, perhaps multiple times:
>>> api.apply(overlay=OVERLAY_ES)
>>> api.apply(overlay=OVERLAY_MONITOR)
# or via a list
>>> api.apply(overlays=[OVERLAY_ES, OVERLAY_MONITOR])
# or a function
>>> overlay(api, OVERLAY_ES)
>>> overlay(api, OVERLAY_MONITOR)
>>> overlay(api, overlays=[OVERLAY_ES, OVERLAY_MONITOR])
#
# further API behavior
>>> api.documentation
[Documentation(title='Introducción'), Documentation(title='Licencias')]
>>> books = api.resources[0]
>>> books
ResourceNode(method='get', path='/books')
>>> books.description
'La colección de libros de la biblioteca'
>>>
>>> api = ramlfications.parse(RAML_FILE, version='1.0', overlay=OVERLAY_MONITOR)
>>> monitor_type = api.annotation_types[0]
AnnotationType(name='monitor')
>>> dir(monitor_type)  # skipping dunder methods
['frequency',
'script'
]
>>> dir(monitor_type.frequency) # skipping dunder methods
['interval',
'unitOfMeasure'
]
>>> monitor_type.frequency.interval.type
int  # or 'integer'
>>> monitor_type.frequency.unitOfMeasure
# a new Enum object type?
Enum(['seconds', 'minutes', 'hours'])
# or just a simple list
['seconds', 'minutes', 'hours']
>>> monitor_type.script.type
str  # or 'string'
>>> books = api.resources[0]
>>> books.annotations
[Annotation(name='monitor')]
>>> mon = books.annotations[0]
>>> mon.frequency.interval
5
>>> mon.frequency.unitOfMeasure
'minutes'
>>> mon.script
'randomBooksFetch'
```

