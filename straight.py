# -*- coding: utf-8 -*-


#インポート------------------------------------------------------------------------
from __future__ import unicode_literals, print_function
import matplotlib.pyplot as plt
import cv2
from datetime import datetime as dt

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
    print(velocity, "cm/s")
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
        drawProb = 150 #[frame/１点] 点をプロットする頻度の逆数
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
#ステータスを描画したウィンドウを消去する関数------------------------------------------------
def ClrWindow():
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    plt.clf()

#メイン関数-----------------------------------------------------------------------
if __name__ == "__main__":
    GoStraight(2)  #←引数はサブゴールまでの距離
    ClrWindow()
    GoStraight(5)
    ClrWindow()
