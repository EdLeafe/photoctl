#!/usr/bin/env python3

FNAME = "/home/pi/.photoctl"
try:
    with open(FNAME, "r") as ff:
        curr = ff.read().strip()
except IOError:
    # Create the file
    open(FNAME, "w+")
    curr = "STOP"

new = "STOP" if curr == "START" else "START"

with open(FNAME, "w") as ff:
    ff.write(new)
print(new)
