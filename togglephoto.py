#!/usr/bin/env python

with open("/home/ed/.photoctl", "r") as ff:
    curr = ff.read().strip()

new = "STOP" if curr == "START" else "START"

with open("/home/ed/.photoctl", "w") as ff:
    ff.write(new)
