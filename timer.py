# -*- coding: utf-8 -*-
from datetime import datetime as dt
import sys, time

startTime = dt.now().timestamp()

while True:
    getTime = dt.now().timestamp()
    elapsedTime = getTime - startTime
    elapsedTime = round(elapsedTime, 2)

    sys.stdout.write("\r%s sec." % elapsedTime)
    sys.stdout.flush()
    time.sleep(0.01)
