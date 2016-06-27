# -*- coding: utf-8 -*-

#インポート-----------------------------------------------------------------------
from __future__ import unicode_literals, print_function
import cv2
import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np

#探索関数
def RouteSearching(pointX,PointY):
    #mapの読み込み-------------------------------------------------------------------
    mapData = "./img/testmap1.png"                           #マップデータPATH
    mapIm = cv2.imread(mapData) 
    
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
    cv2.imshow("map",mapIm)
    cv2.waitKey(500)
    startPointSet = int(input(">>>  Where is Start Point?   ")) 
    endPointSet = int(input(">>>  Where is End Point?   "))
    cv2.destroyWindow("map")
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
#    endPoint = endPointSet
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
    cv2.waitKey(800)
    return throughPoint,point
#移動距離計算----
def CalculateDistance(throughPoint,place,pointX,pointY,point):
    startPoint = np.array([pointX[throughPoint[place]],pointY[throughPoint[place]]])
    endPoint = np.array([pointX[throughPoint[place + 1]],pointY[throughPoint[place + 1]]])

    disSubgoal = np.linalg.norm(endPoint - startPoint) * 0.01
    
    
    mapData = "./img/testmap1.png"                           #マップデータPATH
    mapIm = cv2.imread(mapData) 
    cv2.line(mapIm, point[throughPoint[place]],point[throughPoint[place + 1]], (0, 255, 0),thickness=2)
    cv2.imshow("CurrentPlace",mapIm)
    cv2.waitKey(10)
    
    return disSubgoal

    
#移動距離・出力を描画する関数---------------------------------------------------------
def DrawNum(myWay,setWay,motor,velocity):
    power = round(motor * 100,3)
    im = cv2.imread("./img/screen.jpg")
    text1 = ("moving distance: " + str(round(myWay,3)) + " m")
    cv2.putText(im,text1,(5,40),cv2.FONT_HERSHEY_PLAIN, 2,(0,0,0),2)
    text2 = ("Target distance: " + str(round(setWay,3)) + " m    power:" + str(power) + "%")
    cv2.putText(im,text2,(5,80),cv2.FONT_HERSHEY_PLAIN, 2,(0,0,0),2)
    text3 = ("Velocity: " + str(round(velocity, 3)) + "cm/s")
    cv2.putText(im,text3,(5,120),cv2.FONT_HERSHEY_PLAIN, 2,(0,0,0),2)
    cv2.imshow("Status",im)
    cv2.waitKey(1)
    
#移動の軌跡・出力を描画する関数--------------------------------------------------------
def DrawTrack(myWay,frame,motor,drawFlg):
#    print(myWay)    
    plt.plot(frame, myWay, color="k",marker="o",markersize=10,label="distance")
    plt.plot(frame, motor, color="b",marker="o",markersize=10,label="power")
    
    if drawFlg == 0:
        plt.legend(bbox_to_anchor=(0.28, 1), loc='bottom left', borderaxespad=0)

    plt.pause(0.01)
    
#速度を計算する関数----------------------------------------------------------------
def Velocity(myWay,drawProb,preMyWay,preTime):
    getTime = dt.now().timestamp()
    timeInterval = getTime - preTime
    velocity = (myWay - preMyWay)/timeInterval * 100
#    print(velocity, "cm/s")
    #print(timeInterval)
    preMyWay = myWay
    preTime = getTime
    return velocity,preMyWay,preTime

#決められた距離だけ直進する処理をする関数-------------------------------------------------
def GoStraight(setWay=5):
    resolution = 180 #エンコーダの分解能
    lowMotorPow = 0.15 #停止地点近辺での出力(任意)
    #初期化
    pulse = 0
    frame = 0
    preMyWay = 0
    myWay = 0
    gainMotor = 0.001
    motorPow = 1.0
    drawFlg = 0
    preTime = 0
    lowMotorFlg = 0

    #始動
    motor = 0
    while 1:
        frame += 1
    #  ゆっくり始動               #
        #print("Going straight")
        if myWay < 0.5:
            if motor < 1:
                motor += gainMotor
        else:
            if lowMotorFlg == 0:
                motor = motorPow
            else:
                motor = lowMotorPow
    #                        #
        ccm = 0.102 * 3.14159 #[m] 円周の長さ
        pulse += motor*1 #Get Pulse
        angle = pulse * resolution/360 #[deg]
        myWay = ccm * angle/360
        restWay = setWay - myWay

    #各種描画関数を任意のフレーム毎に呼び出す
        drawProb = 200 #[frame/１点] 点をプロットする頻度の逆数
        drawOrNot = frame % drawProb
        if drawOrNot == 0:
            velocity,preMyWay,preTime = Velocity(myWay,drawProb,preMyWay,preTime)
            DrawTrack(myWay,frame,motor,drawFlg)
            drawFlg = 1
            DrawNum(myWay,setWay,motor,velocity)
            
    #ループ処理(条件分岐)
        if restWay <= 0:
            motor = 0
            print("complete")
            DrawTrack(myWay,frame,motor,drawFlg)
            DrawNum(myWay,setWay,motor,velocity)
            break
        
        if motor > 0 and restWay <= 0.5:
#            print("減速中")
            motorPow -=  0.00022*(1/(restWay+0.1))
        if motor < lowMotorPow and restWay <= 0.5:
            lowMotorFlg = 1
#ステータスを描画したウィンドウを消去する関数---------------------------------------------
def ClrWindow():
    cv2.waitKey(50)
    cv2.destroyAllWindows()
    plt.clf()


#メイン関数-----------------------------------------------------------------------
if __name__ == "__main__":
    #DEFINE
    capChr = [chr(i) for i in range(65,65+26)]#Num2Chr
    pointX = [433,81,153,87,161,362,181]
    pointY = [163,162,39,315,359,254,447]
    #RUNNING
    throughPoint,point = RouteSearching(pointX,pointY)
    for place in range(len(throughPoint)-1):
        disSubgoal = CalculateDistance(throughPoint,place,pointX,pointY,point)
        GoStraight(disSubgoal)#(disSubgoal)
        ClrWindow()
        print("CurrentPlace=",capChr[throughPoint[place+1]])
    print("////////////////////////////// \n    All running completed \n////////////////////////////// \n")
