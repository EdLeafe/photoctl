#!/usr/bin/env python

with open(".photoctl", "r") as ff:
    curr = ff.read().strip()

new = "STOP" if curr == "START" else "START"

with open(".photoctl", "w") as ff:
    ff.write(new)
