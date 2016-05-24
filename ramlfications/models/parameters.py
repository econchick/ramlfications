# -*- coding: utf-8 -*-
# Copyright (c) 2016 Spotify AB

from __future__ import absolute_import, division, print_function

import attr

from .base import BaseParameter, BaseParameterAttrs
from ramlfications.validate import *  # NOQA


@attr.s
class URIParameter(BaseParameter):
    """
    URI parameter with properties defined by the RAML specification's \
    "Named Parameters" section, e.g.: ``/foo/{id}`` where ``id`` is the \
    name of the URI parameter.
    """
    required = attr.ib(repr=False, default=True)
    type         = attr.ib(repr=False, default="string")


@attr.s
class QueryParameter(BaseParameter):
    """
    Query parameter with properties defined by the RAML specification's \
    "Named Parameters" section, e.g. ``/foo/bar?baz=123`` where ``baz`` \
    is the name of the query parameter.
    """
    required     = attr.ib(repr=False, default=False)
    type         = attr.ib(repr=False, default="string")


@attr.s
class FormParameter(BaseParameter):
    """
    Form parameter with properties defined by the RAML specification's
    "Named Parameters" section. Example:

        ``curl -X POST https://api.com/foo/bar -d baz=123``

    where ``baz`` is the Form Parameter name.
    """
    required     = attr.ib(repr=False, default=False)
    type         = attr.ib(repr=False, default="string")


@attr.s
class Header(BaseParameter):
    """
    Header with properties defined by the RAML spec's 'Named Parameters'
    section, e.g.:

        ``curl -H 'X-Some-Header: foobar' ...``

    where ``X-Some-Header`` is the Header name.

    :param str type: Primative type of parameter. Defaults to ``string`` if \
        not set.
    :param str method: HTTP method for header, or ``None``
    """
    type         = attr.ib(repr=False, default="string", validator=header_type)
    method       = attr.ib(repr=False, default=None)
    required     = attr.ib(repr=False, default=False)


@attr.s
class Body(BaseParameterAttrs):
    """
    Body of the request/response.

    :param str mime_type: Accepted MIME media types for the body of the \
        request/response.
    :param dict raw: All defined data of the item
    :param dict schema: Body schema definition, or ``None`` if not set. \
        Can not be set if ``mime_type`` is ``multipart/form-data`` \
        or ``application/x-www-form-urlencoded``
    :param dict example: Example of schema, or ``None`` if not set. \
        Can not be set if ``mime_type`` is ``multipart/form-data`` \
        or ``application/x-www-form-urlencoded``
    :param dict form_params: Form parameters accepted in the body.
        Must be set if ``mime_type`` is ``multipart/form-data`` or \
        ``application/x-www-form-urlencoded``.  Can not be used when \
        schema and/or example is defined.
    """
    mime_type   = attr.ib(init=True, validator=body_mime_type)
    schema      = attr.ib(repr=False, validator=body_schema)
    example     = attr.ib(repr=False, validator=body_example)
    form_params = attr.ib(repr=False, validator=body_form)


@attr.s
class Response(BaseParameterAttrs):
    """
    Expected response parameters.

    :param int code: HTTP response code.
    :param dict raw: All defined data of item.
    :param str description: Response description, or ``None``.
    :param list headers: List of :py:class:`.Header` objects, or ``None``.
    :param list body: List of :py:class:`.Body` objects, or ``None``.
    :param str method: HTTP request method associated with response.
    """
    code     = attr.ib(validator=response_code)
    desc     = attr.ib(repr=False)
    headers  = attr.ib(repr=False)
    body     = attr.ib(repr=False)
    method   = attr.ib(default=None)