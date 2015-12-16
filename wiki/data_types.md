# Data Types

1. [Data Types as described in the RAML spec](#data-types-as-described-in-the-raml-spec)
2. [Broad Implementation TODOs](#broad-implementation-todos)
3. [Where to start](#where-to-start)
4. [Proposed API behavior](#proposed-api-behavior)

Related issues:



## Data Types as described in the RAML spec

* Types are similar to Java classes
    * But borrow additional features from JSON Schema, XSD, and more expressive object oriented languages
* You can define Types that inherit from other Types
    * Multiple inheritance is allowed
* Types are split into four families: scalars, objects, externals and arrays
* Types can define two types of members: properties and facets. Both are inherited
    * Properties are regular object oriented properties
    * Facets are special "configurations" that let you specialize types based on characteristics of their values. For example: minLength, maxLength
* Only object types can declare properties. But all types can declare facets
* The way you specialize a scalar type is by implementing facets ( giving already defined facets a concrete value )
* The way you specialize an object type is by defining properties

## Broad Implementation TODOs

* Parse similar to resource types & traits with own object, applying to resources, handling inheritance
* Handle [shortcuts & syntactic sugar](http://docs.raml.org/specs/1.0/#raml-10-spec-shortcuts-and-syntactic-sugar) appropriately
* Associate keyword `type` in the body, headers, & query/URI parameters part of a RAML file, and be able to parse either primative types (e.g. `string`, `integer`, etc) AND user-defined types (e.g. `User`, `Post`)
* Support both inline & separated definitions
* Parse [Union Types](http://docs.raml.org/specs/1.0/#raml-10-spec-union-types) & [Discriminators](http://docs.raml.org/specs/1.0/#raml-10-spec-runtime-polymorphism-discriminators-)
* Parse custom scalar types
* Parse [type expressions](http://docs.raml.org/specs/1.0/#raml-10-spec-type-expressions)
* Parse `example` and `examples`

## Where to start

These are educated suggestions, and more meant for developers unfamiliar with the `ramlfications` package and are wanting to contribute.

* A new `DataType` object should probably be defined in `ramlfications/raml.py`
* A property called `data_type` should be supported in the following objects, defined in `ramlfications/parameters.py`:
    - URI parameters
    - Query parameters
    - Request headers
    - Response headers
    - Request body
    - Response body
* Nota bene: there is already a `type` parameter for many/all of the above parameter objects
* In `ramlfications/parser.py`, there should be a function that creates all data types define in a provided RAML file (including any external RAML/JSON/XML file it may `!include`/refer to), and be called from within `parse_raml`
* `ramlfications/validate.py` should ensure the file header of `#%RAML 1.0 DataType`
* Not sure if `ramlfications/loader.py` should be affected in any way; perhaps if we want to do anything special with the file header of `#%RAML 1.0 DataType`
* Tests for everything, of course!

Some examples (I think most of them are only `RAML 0.8` right now) for testing and debugging can be found [here](http://docs.raml.org/apis/).

### Questions

* Should there be a property called `data_types` attached to the Root Node, which holds a list of `DataType` objects? Not sure if one has the ability to declare inline types, as Data Types don't necessarily have to be defined in the API Root of the RAML file.



## Proposed API Behavior

### Input

Main RAML file, `api.raml` (snippet):

```RAML
#%RAML 1.0
title: Spotify Web API
version: v1
baseUri: http://api.spotify.com/{version}
mediaType: application/json
uses:
  responseObjects: !include libraries/types.raml
/album:
  get:
    responses:
      200:
        body:
          application/json:
            type: responseObjects.libraries.types.Album
```

Referred library of Data types, `libraries/types.raml`:

```RAML
#%RAML 1.0 Library
types:
  Album: !include ./album.raml
  AlbumSimple: !include ./album_simple.raml
```

Referred Data Type, `album.raml`:

```RAML
#%RAML 1.0 DataType
type: AlbumSimple
displayName: Full Album Object
properties:
  artists: ArtistSimple[]  # would pull in ArtistSimple DataType
  copyrights: Copyright[]  # would pull in Copyright DataType
  external_ids: ExternalId  # would pull in ExternalId DataType
  genres:
    type: string[]
    description: |
      A list of the genres used to classify the album. If not yet classified,
      the array is empty.
    example: ["Prog Rock", "Post-Grunge"]
  popularity:
    type: integer
    description: |
      The popularity of the album. The value will be between 0 and 100,
      with 100 being the most popular. The popularity is calculated from
      the popularity of the album's individual tracks.
  tracks:
    type: Page  # would pull in Page DataType
    (pagedObject): TrackSimple
    description: The tracks of the album.
```

Referred Data Type (and the Data Type from which `album.raml` inherits), `salbum_simple.raml`:

```RAML
#%RAML 1.0 DataType
type: object
displayName: Simple Album Object
properties:
  album_type:
    type: string
    enum: ["album", "single", "compilation"]
    description: The type of the album: one of "album", "single", or "compilation".
  available_markets:
    type: string[]
    description: |
      The markets in which the album is available: [ISO 3166-1 alpha-2 country
      codes](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Note that an album
      is considered available in a market when at least 1 of its tracks is
      available in that market.
  external_urls: ExternalUrl
  href:
    type: string
    description: A link to the Web API endpoint providing full details of the album.
  id: SpotifyId
  images: Image[]
  name:
    type: string
    description: The name of the album.
  type:
    type: string
    default: "album"
  uri: SpotifyUri
```

### Expected Output

I would imagine the Python objects/behavior would look as follows:

```python
>>> RAML_FILE = "api.raml"
>>> api = ramlfications.parse(RAML_FILE, version="1.0")
>>> api.title
"Spotify Web API"
>>> api.resources
[ResourceNode(method='get', path='/album')]
>>> album = api.resources[0]
>>> album.responses
[Response(code='200')]
>>> resp = album.responses[0]
>>> resp.body
[Body(mime_type='application/json')]
>>> body = resp.body[0]
>>> body.data_type
DataType(name='Album')
>>> body.schema
# snipped example
# currently `body.schema` returns OrderedDicts
# but I could be convinced to do `jsonschema` objects for application/json
# and `lxml` objects for application/xml response bodies per issue #15
OrderedDict([('artists', [OrderedDict([('type', ...), ...]))]), ('copyright', [OrderedDict([('type', ...), ...])]), ('external_ids', ...), ('genres', [OrderedDict([('type', 'string[]'), ('description', 'The popularity of...'), ...)])]), ...])
>>> album = data.data_type
>>> album.family
'object'  # or scalar, array,  or external
>>> dir(album)  # skipping over the dunders
['schema',
'type',
'example',
'examples',
'display_name',
'description',
'annotation_name',
'properties',  # start of object-family-specific properites
'min_properties',
'max_properties',
'addl_properties',
'pattern_properties',
'discriminator',
'discriminator_value'
]
```
