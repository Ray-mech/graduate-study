# coding: utf-8
#インポート-----------------------------------------------------------------------
import cv2
 #import numpy as np


#mapの読み込み-------------------------------------------------------------------
mapData = "./img/map.png"                           #マップデータPATH
mapIm = cv2.imread(mapData) 
 
#mapData1のサブゴールリスト
pointX = [433,81,153,87,161,362,181]
pointY = [163,162,39,315,359,254,447]



#point設定---------------------------------------------------------------------
pointQty = len(pointX)
point= [0]*pointQty
# upper-case A-Z
capChr = [chr(i) for i in range(65,65+26)]
for i in range(pointQty):
    point[i] = pointX[i], pointY[i]
    print("point"+str(i)+"  ",capChr[i],point[i])
print("\n")
#経路探索(設定・計算)
#//////////////////////
startPointSet = 5 
endPointSet = 2 
#//////////////////////
# A 0   (point CHARACTER to NUMBER list)
# B 1
# C 2
# D 3
# E 4
# F 5
# G 6
# H 7
# I 8
# J 9
# K 10

startPoint = startPointSet
endPoint = endPointSet
throughPoint = []
adjacent = [
#     A   B   C   D   E   F   G   
    [ 0,  1,  0,  0,  0,  0,  0 ],   # A(0)
    [ 1,  0,  1,  1,  0,  0,  0 ],   # B(1)
    [ 0,  1,  0,  0,  0,  0,  0 ],   # C(2)
    [ 0,  1,  0,  0,  1,  0,  0 ],   # D(3)
    [ 0,  0,  0,  1,  0,  1,  1 ],   # E(4)
    [ 0,  0,  0,  0,  1,  0,  0 ],   # F(5)   
    [ 0,  0,  0,  0,  1,  0,  0 ],   # G(6)              隣接行列
]
MAX_SIZE = 7
MAX_VALUE = 0x10000000
visited = [False] * MAX_SIZE
cost = [MAX_VALUE] * MAX_SIZE
prev = [None] * MAX_SIZE
cost[startPoint] = 0
prev[startPoint] = startPoint
while True:
    min = MAX_VALUE
    next = -1
    visited[startPoint] = True
    # 頂点の選択
    for i in range(MAX_SIZE):
        if visited[i]:
            continue
        if adjacent[startPoint][i]:
            d = cost[startPoint] + adjacent[startPoint][i]
            if d < cost[i]:
                cost[i] = d
                prev[i] = startPoint
        if min > cost[i]:
            min = cost[i]
            next = i
    startPoint = next

    if next == -1: 
        break
    
#経路探索(throughPointの作成)
throughPoint.append(endPointSet)
pre = prev[endPointSet]
while True:
    if pre == startPointSet:
        throughPoint.append(pre)
        break
    else:
        throughPoint.append(pre)
        pre = prev[pre]

throughPoint.reverse() #throughPointはEndから代入していたので、逆順にする

startPointChr = capChr[startPointSet]
endPointChr = capChr[endPointSet]
throughPointChr = []
for i in range(len(throughPoint)):
    throughPointChr.append(capChr[throughPoint[i]])
print("SETTING   start:%d(%s)  end:%d(%s)" % (startPointSet,startPointChr,endPointSet,endPointChr))
print("RESULT    "+str(throughPoint),"  ("+str(throughPointChr)+")")

#直線の描画
for i in range(len(throughPoint)-1):
    cv2.line(mapIm, point[throughPoint[i]],point[throughPoint[i+1]], (0, 0, 255),thickness=2)


cv2.imshow("window",mapIm)
cv2.waitKey(0)
