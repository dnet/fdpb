#!/usr/bin/env python

import os
import sys

for pid in sys.argv[1:]:
    fds = os.listdir('/proc/{0}/fd'.format(pid))
    for fd in fds:
        link = os.readlink('/proc/{0}/fd/{1}'.format(pid, fd))
        if link.startswith('/dev/') or link.startswith('pipe:[') or os.path.isdir(link):
            continue
        print link
        fdinfo = file('/proc/{0}/fdinfo/{1}'.format(pid, fd)).read()
        pos = int(fdinfo.split('\t', 1)[1].split('\n', 1)[0])
        size = os.path.getsize(link)
        print '{0:3}% {1}/{2}'.format(pos * 100 / size, pos, size)
