# import Lib
import numpy as np
import cv2

import time   #Provide the time to boot Camera

cap = cv2.VideoCapture(0)   #VideoCapture object a Webcam

time.sleep(2)   #boot Time for Camera

background = 0   #Background image 1

for i in range(30):     
    ret, background = cap.read()   #Ret 30 iteration Read true/false & read BG

while(cap.isOpened()):  #Till camera is open
    ret, img = cap.read()     #Main image processing operation

    if not ret:
        break       #cap.read off then break
    #Converting from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   #Hue Saturation Value <2^8= 255

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    m1 = cv2.inRange(hsv, lower_red, upper_red)  #Separating the cloak part Or Masking the image 

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    m2 = cv2.inRange(hsv, lower_red, upper_red)  #170 - 180

    m1 = m1 + m2   #OR 1 or X

    m1 = cv2.morphologyEx(m1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)   #Noise Removal
    m1 = cv2.morphologyEx(m1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    m2 = cv2.bitwise_not(m1)    #Except the cloak

    res1 = cv2.bitwise_and(background, background, mask=m1)   #Used for Segmantation of the color
    res2 = cv2.bitwise_and(img, img, mask=m2)  #Used to substitute the cloak part

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow('Magic Cloak !!', final_output)
    k = cv2.waitKey(10)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
