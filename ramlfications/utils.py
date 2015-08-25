# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function


import json
import logging
import os
import sys

import xmltodict

PYVER = sys.version_info[:3]

if PYVER == (2, 7, 9) or PYVER == (3, 4, 3):  # NOCOV
    import six.moves.urllib.request as urllib
    import six.moves.urllib.error as urllib_error
    URLLIB = True
    SECURE_DOWNLOAD = True
else:
    try:  # NOCOV
        import requests
        URLLIB = False
        SECURE_DOWNLOAD = True
    except ImportError:
        import six.moves.urllib.request as urllib
        import six.moves.urllib.error as urllib_error
        URLLIB = True
        SECURE_DOWNLOAD = False

from .errors import MediaTypeError


IANA_URL = "https://www.iana.org/assignments/media-types/media-types.xml"


def load_schema(data):
    """
    Load Schema/Example data depending on its type (JSON, XML).

    If error in parsing as JSON and XML, just returns unloaded data.

    :param str data: schema/example data
    """
    try:
        return json.loads(data)
    except Exception:  # POKEMON!
        pass

    try:
        return xmltodict.parse(data)
    except Exception:  # GOTTA CATCH THEM ALL
        pass

    return data


def setup_logger(key):
    """General logger"""
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    msg = "{key} - %(levelname)s - %(message)s".format(key=key)
    formatter = logging.Formatter(msg)
    console.setFormatter(formatter)

    log.addHandler(console)
    return log


def _requests_download(url):
    """Download a URL using ``requests`` library"""
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        msg = "Error downloading from {0}: {1}".format(url, e)
        raise MediaTypeError(msg)


def _urllib_download(url):
    """Download a URL using ``urllib`` library"""
    try:
        response = urllib.urlopen(url)
    except urllib_error.URLError as e:
        msg = "Error downloading from {0}: {1}".format(url, e)
        raise MediaTypeError(msg)
    return response.read()


def download_url(url):
    """
    General download function, given a URL.

    If running 2.7.8 or earlier, or 3.4.2 or earlier, then use
    ``requests`` if it's installed.  Otherwise, use ``urllib``.
    """
    log = setup_logger("DOWNLOAD")
    if SECURE_DOWNLOAD and not URLLIB:
        return _requests_download(url)
    elif SECURE_DOWNLOAD and URLLIB:
        return _urllib_download(url)
    msg = ("Downloading over HTTPS but can not verify the host's "
           "certificate.  To avoid this in the future, `pip install"
           " \"requests[security]\"`.")
    log.warn(msg)
    return _urllib_download(url)


def _xml_to_dict(response_text):
    """Parse XML response from IANA into a Python ``dict``."""
    try:
        return xmltodict.parse(response_text)
    except xmltodict.expat.ExpatError as e:
        msg = "Error parsing XML: {0}".format(e)
        raise MediaTypeError(msg)


def _extract_mime_types(registry):
    """
    Parse out MIME types from a defined registry (e.g. "application",
    "audio", etc).
    """
    mime_types = []
    records = registry.get("record", {})
    reg_name = registry.get("@id")
    for rec in records:
        mime = rec.get("file", {}).get("#text")
        if mime:
            mime_types.append(mime)
        else:
            mime = rec.get("name")
            if mime:
                hacked_mime = reg_name + "/" + mime
                mime_types.append(hacked_mime)
    return mime_types


def _parse_xml_data(xml_data):
    """Parse the given XML data."""
    registries = xml_data.get("registry", {}).get("registry")
    if not registries:
        msg = "No registries found to parse."
        raise MediaTypeError(msg)
    if len(registries) is not 9:
        msg = ("Expected 9 registries but parsed "
               "{0}".format(len(registries)))
        raise MediaTypeError(msg)
    all_mime_types = []
    for registry in registries:
        mime_types = _extract_mime_types(registry)
        all_mime_types.extend(mime_types)

    return all_mime_types


def _save_updated_mime_types(output_file, mime_types):
    """Save the updated MIME Media types within the package."""
    with open(output_file, "w") as f:
        json.dump(mime_types, f)


def update_mime_types():
    """
    Update MIME Media Types from IANA.  Requires internet connection.
    """
    log = setup_logger("UPDATE")

    log.debug("Getting XML data from IANA")
    raw_data = download_url(IANA_URL)
    log.debug("Data received; parsing...")
    xml_data = _xml_to_dict(raw_data)
    mime_types = _parse_xml_data(xml_data)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(current_dir, "data")
    output_file = os.path.join(data_dir, "supported_mime_types.json")

    _save_updated_mime_types(output_file, mime_types)

    log.debug("Done! Supported IANA MIME media types have been updated.")


def _resource_type_lookup(assigned, root):
    """
    Returns ``ResourceType`` object

    :param str assigned: The string name of the assigned resource type
    :param root: RAML root object
    """
    res_types = root.resource_types
    if res_types:
        res_type_obj = [r for r in res_types if r.name == assigned]
        if res_type_obj:
            return res_type_obj[0]


NAMED_PARAMS = [
    "displayName", "description", "type", "enum", "pattern", "minLength",
    "maxLength", "minimum", "maximum", "example", "default", "required",
    "repeat"
]


def _resource_type_param_inheritance(inherited, node, method, attribute):
    """
    Returns attribute with preference for when resource node explicitly
    defines it.

    :param inherited: ``ResourceType`` object
    :param node: ``Resource`` dictionary
    :param str method: method of resource endpoint
    :param str attribute: Resource attribute looking to parse
    """
    attr = None
    try:
        print(node)
        print(method)
        print(attribute)
        attr = node.get(method).get(attribute)
        print(attr)
        if attr is None:
            raise AttributeError
    except AttributeError:
        try:
            if inherited.method == method:
                attr = getattr(inherited, attribute, None)
        except AttributeError:
            pass
    return attr
