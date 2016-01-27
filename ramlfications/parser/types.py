# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function
import attr
import copy
from six import MAXSIZE
from six import iteritems

from ..errors import UnknownTypeError
from ..parameters import Content

__type_registry = {}

def type_class(klass):
    if klass.type is not None:
        __type_registry[klass.type] = klass
    return klass

def create_type(name, raml_def):
    # Work on a copy. We will pop the type. Don't modify the raw raml object.
    raml_def = copy.copy(raml_def)

    # spec:
    # string is default type when nothing else defined
    typeexpr = raml_def.pop('type', 'string')

    if typeexpr in __type_registry:
        return __type_registry[typeexpr](name=name, **raml_def)
    else:
        # we start simple, type expressions are for another commit
        raise UnknownTypeError("{0} type expression is not supported or not defined".format(typeexpr))

@attr.s
class BaseType(object):
    name            = attr.ib()
    description     = attr.ib(default="", repr=False, convert=Content)
    type            = None


@attr.s
class Property(object):
    required                 = attr.ib(default=None, repr=False)
    default                  = attr.ib(default=None, repr=False)
    type                     = attr.ib(default="string")

def parse_properties(properties):
    # @todo: should parse k for syntax sugar
    return dict([(k, Property(**v))
        for k, v in iteritems(properties)])

@type_class
@attr.s
class ObjectType(BaseType):
    type                 = "object"
    properties           = attr.ib(default=None, convert=parse_properties)
    minProperties        = attr.ib(repr=False, default=0)
    maxProperties        = attr.ib(repr=False, default=MAXSIZE)
    additionalProperties = attr.ib(repr=False, default=None)
    patternProperties    = attr.ib(repr=False, default=None)
    discriminator        = attr.ib(repr=False, default=None)
    discriminatorValue   = attr.ib(repr=False, default=None)

@type_class
@attr.s
class StringType(BaseType):
    type     = "string"
