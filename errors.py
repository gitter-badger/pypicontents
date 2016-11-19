
import os
import re
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

    jsondict = {'setup': [], 'api': [], 'nodownloads': []}
    basedir = os.path.dirname(__file__)
    logdir = os.path.join(basedir, 'logs')
    errors = os.path.join(basedir, 'errors.json')

    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    for logfile in find_files(logdir, '*.log'):
        with open(logfile) as l:
            content = l.read()
            setuplist = re.findall(r'\[ERROR\]\s*\((.*?)\)', content)
            apilist = re.findall(r'\[WARNING\]\s*\((.*?)\)\s*XMLRPC\s*API', content)
            nodownloadslist = re.findall(r'\[WARNING\]\s*\((.*?)\)\s*This\s*package', content)
            jsondict['setup'].extend(setuplist)
            jsondict['api'].extend(apilist)
            jsondict['nodownloads'].extend(nodownloadslist)

    with open(errors, 'w') as e:
        e.write(json.dumps(jsondict, separators=(',', ': '),
                           sort_keys=True, indent=4))
