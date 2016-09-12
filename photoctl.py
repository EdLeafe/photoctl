#!/usr/bin/env python
from __future__ import print_function

import datetime
import os
from subprocess import Popen, PIPE

HOMEDIR = "/home/ed/projects/photoviewer"
DATE_FMT = "%Y.%m.%d %H:%M:%S"

def runproc(cmd):
    proc = Popen([cmd], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE,
            close_fds=True)
    stdout_text, stderr_text = proc.communicate()
    return stdout_text, stderr_text


now = datetime.datetime.now().strftime(DATE_FMT)
PHOTODIR = "/home/ed/projects/photoviewer/display"
VIEWER_CMD = "eog -f -s %s"  % PHOTODIR

with open("/home/ed/.photoctl") as ff:
    action = ff.read().strip()
out, err = runproc("pgrep eog")

running = bool(out)

if running and action == "STOP":
    print(now, "Stopping the app")
    os.kill(int(out), 15)
elif not running and action == "START":
    print(now, "Starting the app")
    print(now, "CMD", VIEWER_CMD)
    runproc(VIEWER_CMD)

