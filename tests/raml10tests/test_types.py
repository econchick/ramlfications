# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB
from __future__ import absolute_import, division, print_function

import os

import pytest

from ramlfications.parser import parse_raml
from ramlfications.config import setup_config
from ramlfications.utils import load_file


from tests.base import RAML10EXAMPLES


# Security scheme properties:
# name, raw, type, described_by, desc, settings, config, errors


# as much as possible, those tests are implementing the spec
# the filenames are mapped against
def loadapi(fn):
    ramlfile = os.path.join(RAML10EXAMPLES, fn)
    loaded_raml = load_file(ramlfile)
    conffile = os.path.join(RAML10EXAMPLES, "test_config.ini")
    config = setup_config(conffile)
    return parse_raml(loaded_raml, config)


def test_object():
    api = loadapi("raml-10-spec-object-types.raml")
    exp = "{'Person': ObjectType(name='Person', properties={'name': Property(type='string')})}"
    assert repr(api.types) == exp
