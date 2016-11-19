
import os
import re
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
    stats = os.path.join(basedir, 'stats.txt')

    total = 0
    processed = 0
    updated = 0
    uptodate = 0
    errored = 0
    nodownloads = 0
    api = 0
    notprocessed = 0

    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    for logfile in find_files(logdir, '*.log'):
        with open(logfile) as l:
            content = l.read()
            total += int(re.findall(r'\s*Total\s*number\s*of\s*packages:\s*(\d*)', content)[0])
            processed += int(re.findall(r'\s*Number\s*of\s*processed\s*packages:\s*(\d*)', content)[0])
            updated += int(re.findall(r'\s*Number\s*of\s*updated\s*packages:\s*(\d*)', content)[0])
            uptodate += int(re.findall(r'\s*Number\s*of\s*up-to-date\s*packages:\s*(\d*)', content)[0])
            errored += int(re.findall(r'\s*Number\s*of\s*errored\s*packages:\s*(\d*)', content)[0])
            nodownloads += int(re.findall(r'\s*Number\s*of\s*packages\s*without\s*downloads:\s*(\d*)', content)[0])
            api += int(re.findall(r'\s*Number\s*of\s*packages\s*without\s*response\s*from\s*API:\s*(\d*)', content)[0])
            notprocessed += int(re.findall(r'\s*Number\s*of\s*packages\s*that\s*could\s*not\s*be\s*processed:\s*(\d*)', content)[0])

    with open(stats, 'w') as s:
        s.write('Total number of packages: %s\n' % total)
        s.write('    Number of processed packages: %s\n' % processed)
        s.write('        Number of updated packages: %s\n' % updated)
        s.write('        Number of up-to-date packages: %s\n' % uptodate)
        s.write('        Number of errored packages: %s\n' % errored)
        s.write('        Number of packages without downloads: %s\n' % nodownloads)
        s.write('        Number of packages without response from API: %s\n' % api)
        s.write('    Number of packages that could not be processed: %s\n' % notprocessed)
