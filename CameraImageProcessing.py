# -*- coding: utf-8 -*-
import cv2


def main():
    # Camera caputure
    cap1 = cv2.VideoCapture(0)

    while True:
        im1 = cap1.read()[1]        # Get Frame cam1
        im1_gray = cv2.cvtColor(im1, cv2.COLOR_RGB2GRAY) #　Tran.to gray cam1 

    #　thresholding
        thresh1 = 75
        max_pixel1 = 255
        ret, im1_bin = cv2.threshold(im1_gray,
                                 thresh1,
                                 max_pixel1,
                                 cv2.THRESH_BINARY)
        
    #　Set window
        cv2.imshow("Original",im1)
        cv2.imshow("GrayScale",im1_gray)
        cv2.imshow("Binary",im1_bin)
        # Loop out
        if cv2.waitKey(10) > 0:
            cap1.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
