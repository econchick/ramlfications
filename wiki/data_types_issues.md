# Add support for Data Type

* Support for four family types:
    * [object](http://docs.raml.org/specs/1.0/#raml-10-spec-object-types) including [Map types](http://docs.raml.org/specs/1.0/#raml-10-spec-map-types)
    * [scalar](http://docs.raml.org/specs/1.0/#raml-10-spec-scalar-types)
        * [built-in](http://docs.raml.org/specs/1.0/#raml-10-spec-built-in-scalar-types)
        * [enums](http://docs.raml.org/specs/1.0/#raml-10-spec-enums)
        * [custom scalars](http://docs.raml.org/specs/1.0/#raml-10-spec-customsecurityscheme-scalar-types)
    * [array](http://docs.raml.org/specs/1.0/#raml-10-spec-array-types)
    * [external](http://docs.raml.org/specs/1.0/#raml-10-spec-external-types)
* Supported functionality:
    * Inheritance for [objects](http://docs.raml.org/specs/1.0/#raml-10-spec-object-type-inheritance); mindful of [restrictions](http://docs.raml.org/specs/1.0/#raml-10-spec-inheritance-restrictions)
    * [Type Expression](http://docs.raml.org/specs/1.0/#raml-10-spec-type-expressions)
    * [Union types](http://docs.raml.org/specs/1.0/#raml-10-spec-union-types)
    * [Shortcuts & syntatic sugar](http://docs.raml.org/specs/1.0/#raml-10-spec-shortcuts-and-syntactic-sugar)
    * [Runtime polymorphism](http://docs.raml.org/specs/1.0/#raml-10-spec-runtime-polymorphism-discriminators-)
    * [Examples](http://docs.raml.org/specs/1.0/#raml-10-spec-examples)
    * [Inline declaration](http://docs.raml.org/specs/1.0/#raml-10-spec-inline-type-declarations)
* Data Types support for:
    * URI Parameters
    * Query parameters
    * Request & Response Headers
    * Request & Response Body
        * JSON
        * XML
        * Form
