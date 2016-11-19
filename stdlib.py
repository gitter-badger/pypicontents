import os
import json
import warnings

from sphinx.ext.intersphinx import fetch_inventory


class DummyApp(object):
    def __init__(self, basedir):
        self.srcdir = basedir
        self.warn = warnings.warn
        self.info = lambda *args: []


if __name__ == '__main__':

    jsondict = {}
    basedir = os.path.dirname(__file__)
    stdlib = os.path.join(basedir, 'stdlib.json')

    long_versions = ['2.6.9', '2.7.9', '3.2.6', '3.3.6', '3.4.3', '3.5']
    short_versions = ['.'.join(x.split('.')[:2]) for x in long_versions]

    for version in short_versions:
        url = 'http://docs.python.org/%s/objects.inv' % version
        inventory = fetch_inventory(DummyApp(basedir), '', url)
        modules = sorted(list(inventory.get('py:module').keys()))
        jsondict.update({version: modules})

    with open(stdlib, 'w') as s:
        s.write(json.dumps(jsondict, separators=(',', ': '),
                           sort_keys=True, indent=4))
