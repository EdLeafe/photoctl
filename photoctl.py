#!/usr/bin/env python
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
#VIEWER_CMD = "eog -f -s %s"  % PHOTODIR
VIEWER_CMD = "qiv --display :0 -imtfs %s &"  % PHOTODIR
PYTHON_CMD = "cd %s; python photo.py &" % HOMEDIR
PID_CMD = "ps -ef | grep %s | grep -v grep | awk '{print $2}'"


with open("/home/pi/.photoctl") as ff:
    action = ff.read().strip()
disp_out, err = runproc(PID_CMD % "qiv")
disp_running = bool(disp_out)
python_out, err = runproc(PID_CMD % "photo.py")
python_running = bool(python_out)

if action == "STOP":
    if disp_running:
        print(now, "Stopping the app")
        os.kill(int(disp_out), 15)
    if python_running:
        print(now, "Stopping python controller")
        os.kill(int(python_out), 15)
elif action == "START":
    if not disp_running:
        print(now, "Starting the app")
        print(now, "CMD", VIEWER_CMD)
        runproc(VIEWER_CMD, False)
    if not python_running:
        print(now, "Starting python controller")
        print(now, "CMD", PYTHON_CMD)
        runproc(PYTHON_CMD, False)

