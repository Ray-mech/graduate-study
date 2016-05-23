# -*- coding: utf-8 -*-
import cv2


def main():
    # Camera caputure
    cap1 = cv2.VideoCapture(2)
    cap2 = cv2.VideoCapture(3)



    while(1):
        im1 = cap1.read()[1]        # Get Frame cam1
        im1_gray = cv2.cvtColor(im1, cv2.COLOR_RGB2GRAY) #　Tran.to gray cam1 
        im2 = cap2.read()[1]        # Get Frame cam2
        im2_gray = cv2.cvtColor(im2, cv2.COLOR_RGB2GRAY) #　Tran.to gray cam2

        
    #　thresholding
        #1
        thresh1 = 75
        max_pixel1 = 255
        ret, im1_2value1 = cv2.threshold(im1_gray,
                                 thresh1,
                                 max_pixel1,
                                 cv2.THRESH_BINARY)
        
        #2
        thresh1 = 75
        max_pixel1 = 255
        ret, im2_2value1 = cv2.threshold(im2_gray,
                                 thresh1,
                                 max_pixel1,
                                 cv2.THRESH_BINARY)

    #　Set window
        cv2.imshow("1",im1_2value1)
        cv2.imshow("2",im2_2value1)

        # Loop out
        if cv2.waitKey(10) > 0:
            cap1.release()
            cap2.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
