#!/usr/bin/env python3
from __future__ import print_function

import datetime
import os
from subprocess import Popen, PIPE

HOMEDIR = "/home/pi/projects/photoviewer"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

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
PHOTO_PID_FILE = "%s/photo.pid" % HOMEDIR
with open(PHOTO_PID_FILE) as ff:
    PHOTO_PID = ff.read().strip()
PHOTOAPP_CMD = "cd %s; python3 photo.py &" % HOMEDIR
#PID_CMD = "ps -ef | grep  photo.py | grep -v grep | awk '{print $2}'"
PID_CMD = "ps --no-headers -p %s" % PHOTO_PID
photoapp_out, err = runproc(PID_CMD)
photoapp_running = bool(photoapp_out)

with open("/home/pi/.photoctl") as ff:
    action = ff.read().strip()
if action == "STOP":
    if photoapp_running:
        print(now, "Stopping python controller")
        os.kill(int(photoapp_out), 15)
elif action == "START":
    if not photoapp_running:
        print(now, "Starting python controller")
        print(now, "CMD", PHOTOAPP_CMD)
        runproc(PHOTOAPP_CMD, False)
