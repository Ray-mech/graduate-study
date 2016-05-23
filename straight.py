# -*- coding: utf-8 -*-
#http://qiita.com/hausen6/items/b1b54f7325745ae43e47

#インポート---------------------------------------------------------------
from __future__ import unicode_literals, print_function
import matplotlib.pyplot as plt
import cv2


#移動距離・出力を描画する関数-----------------------------------------------------
def DrawNum(myWay,setWay,motor):
    power = round(motor * 100,3)
    im = cv2.imread("./img/screen.jpg")
    text1 = ("moving distance:" + str(round(myWay,3)) + " m")
    cv2.putText(im,text1,(5,40),cv2.FONT_HERSHEY_PLAIN, 2,(0,0,0),2)
    text2 = ("Target distance:" + str(round(setWay,3)) + " m    power:" + str(power) + "%")
    cv2.putText(im,text2,(5,80),cv2.FONT_HERSHEY_PLAIN, 2,(0,0,0),2)
    cv2.imshow("distance",im)
    cv2.waitKey(1)
    
#移動の軌跡を描画する関数--------------------------------------------------------
def DrawTrack(myWay,frame):
#    print(myWay)    
    plt.plot(frame, myWay, color="k",marker="o",markersize=10)
    plt.pause(0.01)
    
#速度を計算する関数--------------------------------------------------------
def Velocity(myWay,drawProb,preMyWay):
        velocity = (myWay - preMyWay)/drawProb * 100
        print(velocity, "cm/frame")
        preMyWay = myWay
        return velocity,preMyWay

#決められた距離だけ直進する処理をする関数-----------------------------------------
def GoStraight(setWay=5):
    resolution = 180 #エンコーダの分解能
    #初期化
    pulse = 0
    frame = 0
    preMyWay = 0
    myWay = 0
    gainMotor = 0.001
    kp = 0.3
    #始動
    motor = 0
    while 1:
        frame += 1
    #  ゆっくり始動               #
        if motor < 1:
            motor +=gainMotor
    #                        #
        ccm = 0.102 * 3.14159 #[m] 円周の長さ
        pulse += motor*2 #Get Pulse
        angle = pulse * resolution/360 #[deg]
        myWay = ccm * angle/360
        restWay = setWay - myWay



    #各種描画関数を任意のフレーム毎に呼び出す
        drawProb = 100 #[frame/１点] 点をプロットする頻度の逆数
        drawOrNot = frame % drawProb

        if drawOrNot == 0:
            velocity,preMyWay = Velocity(myWay,drawProb,preMyWay)
            DrawTrack(myWay,frame)
            DrawNum(myWay,setWay,motor)

        gainMotor = kp * restWay
    #ループ処理(条件分岐)

        if myWay >= setWay - 0.5:
            if myWay >= setWay - 0.05:
                motor = 0
                print("stop")
                print(myWay)
                break
            elif motor > 0:
                #print("減速中")
#                motor -= 0.0010001 *1/restWay

            else:
                motor +=0.0015


#メイン関数---------------------------------------------------------------
if __name__ == "__main__":
    GoStraight(5)
    cv2.waitKey(0)
