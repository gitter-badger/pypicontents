
import os
import json
import fnmatch


def get_path(path=[]):
    assert type(path) == list
    return os.path.normpath(os.path.realpath(
        os.path.abspath(os.path.join(*path))))


def find_files(path=None, pattern='*'):
    d = []
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(files, pattern):
            if os.path.isfile(os.path.join(directory, filename)):
                if os.path.islink(os.path.join(directory, filename)):
                    d.append(os.path.join(get_path([directory]), filename))
                else:
                    d.append(get_path([directory, filename]))
    return d

if __name__ == '__main__':

    jsondict = {}
    basedir = os.path.dirname(__file__)
    datadir = os.path.join(basedir, 'data')
    pypi = os.path.join(basedir, 'pypi.json')

    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    for jsonfile in find_files(datadir, '*.json'):
        with open(jsonfile) as j:
            jsondict.update(json.loads(j.read() or '{}'))

    with open(pypi, 'w') as c:
        c.write(json.dumps(jsondict, separators=(',', ': '),
                           sort_keys=True, indent=4))
