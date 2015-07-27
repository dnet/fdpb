#!/usr/bin/env python

from argparse import ArgumentParser
from time import sleep
import os

parser = ArgumentParser(description='File descriptor progressbar')
parser.add_argument('pid', nargs='+', type=int, metavar='PID')
parser.add_argument('--watch', type=int, default=0, metavar='N',
        help='Repeat measurements every N seconds')
args = parser.parse_args()

past_pos = {}

while True:
    for pid in args.pid:
        fds = os.listdir('/proc/{0}/fd'.format(pid))
        for fd in fds:
            link = os.readlink('/proc/{0}/fd/{1}'.format(pid, fd))
            if link.startswith('/dev/') or link.startswith('pipe:[') or os.path.isdir(link):
                continue
            print link
            fdinfo = file('/proc/{0}/fdinfo/{1}'.format(pid, fd)).read()
            pos = int(fdinfo.split('\t', 1)[1].split('\n', 1)[0])
            size = os.path.getsize(link)
            pp = past_pos.get((pid, fd, link))
            if pp is not None:
                speed = (pos - pp) / args.watch
                sec = (size - pos) / speed
                prefix = ''
                if speed > 1024:
                    speed /= 1024
                    prefix = 'k'
                if speed > 1024:
                    speed /= 1024
                    prefix = 'M'
                if speed > 1024:
                    speed /= 1024
                    prefix = 'G'
                speed = ' {0:5} {1}B/s'.format(speed, prefix)
                if sec:
                    speed += ' approx {0}:{1:02} left'.format(sec / 60, sec % 60)
            else:
                speed = ''
            print '{0:3}% {1}/{2}{3}'.format(pos * 100 / size, pos, size, speed)
            past_pos[pid, fd, link] = pos
    if not args.watch:
        break
    print '-' * int(os.environ.get('COLUMNS', 80))
    sleep(args.watch)
