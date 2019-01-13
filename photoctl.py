#!/usr/bin/env python3
from __future__ import print_function

import datetime
import os
import six
from subprocess import Popen, PIPE
import time


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


def killapp(pid):
    try:
        os.kill(pid, 15)
    except ProcessLookupError:
        pass


now = datetime.datetime.now().strftime(DATE_FMT)
PHOTO_PID_FILE = "%s/photo.pid" % HOMEDIR
with open(PHOTO_PID_FILE) as ff:
    PHOTO_PID = int(ff.read().strip())
PHOTOAPP_CMD = "cd %s; python3 photo.py &" % HOMEDIR
#PID_CMD = "ps -ef | grep  photo.py | grep -v grep | awk '{print $2}'"
PID_CMD = "ps --no-headers -p %s | awk '{print $2}'" % PHOTO_PID
photoapp_out, err = runproc(PID_CMD)
photoapp_running = bool(photoapp_out)
MAX_HOST_CHECK_INTERVAL = 3600
HOST_CHECKED_FILE = "%s/.host_checked" % HOMEDIR
try:
    mtime = os.stat(HOST_CHECKED_FILE).st_mtime
    if isinstance(mtime, six.string_types):
        mtime = mtime.decode("utf-8")
    mtime = float(mtime)
except FileNotFoundError:
    # Running with an older photo app that doesn't create the file.
    mtime = time.time()
interval = time.time() - mtime
restart = interval > MAX_HOST_CHECK_INTERVAL

with open("/home/pi/.photoctl") as ff:
    action = ff.read().strip()
if action == "PAUSE":
    # Don't make any changes
    exit()
if action == "STOP":
    if photoapp_running:
        print(now, "Stopping python controller")
        killapp(PHOTO_PID)
elif action == "START":
    if restart:
        print(now, "Python controller unresponsive; restarting")
        killapp(PHOTO_PID)
        photoapp_running = False
    if not photoapp_running:
        print(now, "Starting python controller")
        print(now, "CMD", PHOTOAPP_CMD)
        runproc(PHOTOAPP_CMD, False)
