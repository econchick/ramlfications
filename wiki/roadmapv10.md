# RAML v1.0 Roadmap

**CAUTION**: roadmap is currently being worked on & spec'ed out.

All the tasks related to adding [RAML v1.0 specification][ramlv10] support to `ramlfications`.

## Changed

* Security Schemes
* Array-valued properties can be expressed as scalars when only 1 member
* Optionality of `baseUri`
* Overloading rules (not sure what has changed yet)

### Root properties

Adjustment/changes to the following current properties:

* `baseUri` - now optional
* default `mediaType`- must conform to [RFC 6838](https://tools.ietf.org/html/rfc6838)

### Security Schemes

##### Things to think about during implementation

* `describedBy` points to `SecuritySchemaPart` object
* `SecuritySchemaPart` defines `headers`, `responses`, etc
* `FixedUri` value type when defining authentication URLs (e.g. `requestTokenUri` for OAuth 1.0) and should conform to RFC 3986.
* Addition to support `PassThrough` authentication (in addition to OAuth 1 & 2, basic, digest, & custom `x-`)
* Add/confirm ability to parse `null` element when assigning authentication to a resource, e.g. `securedBy: [null, oauth_2_0]

## New

### Root properties

Now must be able to parse:

* `(<annotationName>)`
* `types`
* `annotationTypes`
* `uses`

### Data Types


### Annotations

### Extensions

### Overlays

### Example & Examples


## How to handle compatibility

How should `ramlfications` handle both parsing RAML 0.8 and 1.0 specifications?


[ramlv10]: http://docs.raml.org/specs/1.0/
