# RAMLfications Roadmaps

Want to know what's going on? Want to help out? Please dive in!

Be sure to check out our [task board][taskboard] to see what's being worked on actively, the progress of such tasks, and anything that's available to be picked up and worked on. Please check out the [How to Contribute](https://ramlfications.readthedocs.org/en/latest/contributing.html) documentation for how to contribute to RAMLfications as well as what the labels on issues and the [task board][taskboard] mean.

* [v0.1.9](#ramlfications-v019-roadmap)
* [v0.2.0](#ramlfications-v020-roadmap)

## RAMLfications v0.1.9 Roadmap

**Timeline:** ? Need to finish spec'ing out [RAML v1.0 Roadmap][v1.0roadmap]


### Issues to fix

[Milestone View](https://github.com/spotify/ramlfications/issues?q=is%3Aopen+is%3Aissue+milestone%3A%220.1.9+release%22)

* [Issue 23][23]: Resource type inheritance
* [Issue 37][37]: Preserve order of URI parameters
* [Issue 43][43]: Support optional properties in resource types (not just methods) and traits
* [Issue 56][56]: URI parameters missing if not listed in `uriParameters` property

### PRs to review

* [PR 52][52]: Add class Node List
* [PR 55][55]: Fix how args are passed into pytest in setup.py
* [PR 57][57]: Reqork URI params trait spec/tests
* [PR 65][65]: Raise descriptive LoadRAMLError when invalid JSON data is loaded


## RAMLfications v0.2.0 Roadmap

Timeline: ? Need to finish spec'ing out [RAML v1.0 Roadmap][v1.0roadmap]

### Issues to fix

[Milestone view](https://github.com/spotify/ramlfications/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+milestone%3A%220.2.0+release%22+)
* [Issue 14][14]: Top level schemas are not resolved when assigned to resources
* [Issue 51][51]: Errors aren't collected for multiple of the same item being validated (e.g. multiple protocols)

### Features

* [Issue 3][3]: Handle `!pluralize` and `!singularize` functions to ``<< parameters >>``
* [Issue 2][2]: Parsing & filling in of ``<< parameters >>`` into individual resources
* [Issue 54][54]: Support for RAML spec version 1.0 - see [RAML v1.0 Roadmap][v1.0roadmap] for more detail


[14]: https://github.com/spotify/ramlfications/issues/14
[3]: https://github.com/spotify/ramlfications/issues/3
[2]: https://github.com/spotify/ramlfications/issues/2
[23]: https://github.com/spotify/ramlfications/issues/23
[37]: https://github.com/spotify/ramlfications/issues/37
[43]: https://github.com/spotify/ramlfications/issues/43
[51]: https://github.com/spotify/ramlfications/issues/51
[56]: https://github.com/spotify/ramlfications/issues/56
[52]: https://github.com/spotify/ramlfications/pull/52
[55]: https://github.com/spotify/ramlfications/pull/55
[57]: https://github.com/spotify/ramlfications/pull/57
[65]: https://github.com/spotify/ramlfications/pull/65
[54]: https://github.com/spotify/ramlfications/issues/54
[taskboard]: https://waffle.io/spotify/ramlfications
[v1.0roadmap]: https://github.com/spotify/ramlfications/wiki/RAML-v1.0-Roadmap

