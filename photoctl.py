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
#VIEWER_CMD = "eog -f -s %s"  % PHOTODIR
#VIEWER_CMD = "qiv --display :0 -imtfs %s &"  % PHOTODIR
VIEWER_CMD = "sudo killall fbi; sudo fbi -a --noverbose --cachemem 0 -T 1 -t 30 %s/display.jpg %s/alias1.jpg %s/alias2.jpg" % (PHOTODIR, PHOTODIR, PHOTODIR)
PHOTOAPP_CMD = "cd %s; python3 photo.py &" % HOMEDIR
PID_CMD = "ps -ef | grep %s | grep -v grep | awk '{print $2}'"

with open("/home/pi/.photoctl") as ff:
    action = ff.read().strip()
#disp_out, err = runproc(PID_CMD % "qiv")
disp_out, err = runproc(PID_CMD % "fbi")
disp_running = bool(disp_out)
photoapp_out, err = runproc(PID_CMD % "photo.py")
photoapp_running = bool(photoapp_out)

if action == "STOP":
    if disp_running:
        print(now, "Stopping the app")
#        os.kill(int(disp_out), 15)
        runproc("sudo killall fbi")
    if photoapp_running:
        print(now, "Stopping python controller")
        os.kill(int(photoapp_out), 15)
elif action == "START":
    if not disp_running:
        print(now, "Starting the app")
        print(now, "CMD", VIEWER_CMD)
        runproc(VIEWER_CMD, False)
    if not photoapp_running:
        print(now, "Starting python controller")
        print(now, "CMD", PHOTOAPP_CMD)
        runproc(PHOTOAPP_CMD, False)
