# Annotations

1. [Broad Implementation TODOs](#broad-implementation-todos)
2. [Validation](#validation)
3. [Where to start](#where-to-start)
4. [Proposed API behavior](#proposed-api-behavior)

Related issues:


## Broad Implementation TODOs

* Parse similar to `ResourceType` and `Traits` with own object, applying to resources, data types, resource types, traits, methods
* When handling the assignment of annotations, must parse via strings within parenthesis, e.g. `(foo)`
* Declaration handled in the root of the API definition


## Validation

When extending `ramlfications/validation.py`, be sure to check:

* Appropriate file headers of either `#%RAML 1.0` or `#%RAML 1.0 AnnotationTypeDeclaration`
* Annotations are _not_ inherited when applied to Data Types
* All annotations _must_ be declared in the the API root of the RAML file within `annotationTypes` property
* If `allowedTargets` property is present in the declaration of the annotation, annotations then can *only* be assigned to those particular targets (e.g. traits, body, etc). This requires validation of objects that have applied annotations, not just the validation of the annotation itself
* Valid assigned targets:
    - API root
    - Documentation
    - Resource
    - Method
    - Response
    - Request & Response body
    - Data type
    - Named example (see [issue XX](TODO))
    - Resource type
    - Trait
    - Security Scheme
    - Security Scheme Settings (see [issue XX](TODO))
    - Annotation Type Declaration
    - Library (see [issue XX](TODO))
    - Overlay (see [issue XX](TODO))
    - Extension (see [issue XX](TODO))


## Where to start

These are educated suggestions, and more meant for developers unfamiliar with the `ramlfications` package and are wanting to contribute.

* A new `Annotation` object should probably be defined in `ramlfications/raml.py` parsed from the API root-level `annotationTypes` in the RAML file
* A property called `annotation_types` attached to the Root Node, which holds a list of `Annotation` objects
* A property called `annotation_name` should be supported in the following objects:
    * Within `ramlfications/raml.py`:
        - Root node (in `ramlfications/raml.py`)
        - Resource node (supporting both resource-level annotations as well as a method-level annotations)
        - Resource type node
        - Trait node
        - Data Type (see [issue 69](https://github.com/spotify/ramlfications/issues/69))
        - Annotation (an annotation can be annotated)
    * Within `ramlfications/parameters.py`
        - Documentation
        - Response
        - Body
        - Security Scheme
        - Security Scheme Settings (see [issue XX](TODO))
        - Library (see [issue XX](TODO))
        - Overlay (see [issue XX](TODO))
        - Extension (see [issue XX](TODO))
* In `ramlfications/parser.py`, there should be a function that creates all annotations defined in the provided RAML file (including any external RAML files that are declared via `!include`), and be called from within `parse_raml` function
* Apply the [validation](#validation) rules/checks within `ramlfications/validate.py`
* Not sure if `ramlfications/loader.py` should be affected in any way; perhaps if we want to do anything special with the file header of `#%RAML 1.0 AnnotationTypeDeclaration`
* Annotations _are_ inherited/applied to the endpoint when assigned within a Resource Type or Trait
* Annotations assigned in a Trait are applied to all methods of a Resource that is assigned that Trait
* Resource-level annotation values will overwrite any annotation values inherited from an assigned Resource Type and/or Trait
* Similarly, Resource Type annotations overwrite Trait annotations when applied to a Resource Type or Resource
* Tests! Documentation!

Some examples (I think most of them are only `RAML 0.8` right now) for testing and debugging can be found [here](http://docs.raml.org/apis/).


## Proposed API behavior

**TODO**
