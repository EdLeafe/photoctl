#!/usr/bin/env python
from __future__ import print_function

import os
import datetime

HOMEDIR = "/home/ed/projects/photoviewer"
DATE_FMT = "%Y.%m.%d %H:%M:%S"

now = datetime.datetime.now().strftime(DATE_FMT)

with open("/home/ed/.photoctl") as ff:
    action = ff.read().strip()
os.chdir(HOMEDIR)
with open("photo.pid") as ff:
    pid = int(ff.read().strip())

running = True
try:
    os.kill(pid, 0)
except OSError:
    running = False

if running and action == "STOP":
    print(now, "Stopping the app")
    os.kill(pid, 15)
elif not running and action == "START":
    print(now, "Starting the app")
    cmd = "cd %s; /usr/bin/python %s/photo.py & " % (HOMEDIR, HOMEDIR)
    os.system(cmd)

