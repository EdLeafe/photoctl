#!/usr/bin/env python3
from __future__ import print_function

import datetime
import os
from subprocess import Popen, PIPE

HOMEDIR = "/home/pi/projects/photoviewer"
DATE_FMT = "%Y.%m.%d %H:%M:%S"

def runproc(cmd, wait=True):
    if wait:
        kwargs = dict(stdin=PIPE, stdout=PIPE, stderr=PIPE)
    else:
        kwargs = dict(stdin=None, stdout=None, stderr=None)
    proc = Popen([cmd], shell=True, close_fds=True, **kwargs)
    if wait:
        stdout_text, stderr_text = proc.communicate()
        return stdout_text, stderr_text

now = datetime.datetime.now().strftime(DATE_FMT)
PHOTODIR = "%s/display" % HOMEDIR
PHOTOAPP_CMD = "cd %s; python3 photo.py &" % HOMEDIR
PID_CMD = "ps -ef | grep %s | grep -v grep | awk '{print $2}'"

with open("/home/pi/.photoctl") as ff:
    action = ff.read().strip()
photoapp_out, err = runproc(PID_CMD % "photo.py")
photoapp_running = bool(photoapp_out)

if action == "STOP":
    if photoapp_running:
        print(now, "Stopping python controller")
        os.kill(int(photoapp_out), 15)
elif action == "START":
    if not photoapp_running:
        print(now, "Starting python controller")
        print(now, "CMD", PHOTOAPP_CMD)
        runproc(PHOTOAPP_CMD, False)
