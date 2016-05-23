# -*- coding: utf-8 -*-
#http://qiita.com/hausen6/items/b1b54f7325745ae43e47
from __future__ import unicode_literals, print_function

import matplotlib.pyplot as plt
print("angle",",","myWay")

setWay = 30 #m setWay
nnn = 180 #エンコーダの分解能
pulse = 0
frame = 0
myWay = 0

motor = 1
while 1:
    frame += 1
    enshu = 0.102 * 3.14159 #m
    pulse += 2 #Get Pulse
    angle = pulse * nnn/360 #[deg]
    myWay = enshu * angle/360
    plt.plot(frame, myWay, color="k",marker="o",markersize=10)

    plt.legend()
    plt.pause(0.5)

    if myWay < setWay:
        motor = 1
    else:
        motor = 0
        print("stop")
        break




