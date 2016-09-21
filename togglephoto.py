#!/usr/bin/env python

with open("/home/pi/.photoctl", "r") as ff:
    curr = ff.read().strip()

new = "STOP" if curr == "START" else "START"

with open("/home/pi/.photoctl", "w") as ff:
    ff.write(new)
print(new)
