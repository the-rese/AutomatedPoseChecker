from itertools import count
from turtle import color
import cv2
import numpy as np
import time
import PoseDetectionModule as pm

# Things added in the code:
# 1. called the findAngle function
# 2. used cv2.resize for resizing the frame of the video
# 3. variable count is added to count the number of curls
# 4. direction: 0 -> going up, 1 -> going down. One full curl if it has undergo both direction
# 5. added bar

cap = cv2.VideoCapture('videos/2.mp4')
detector = pm.PoseDetector()
count = 0
direction = 0 
prevTime = 0

while True:
    success, frame = cap.read()
    # frame = cv2.imread('videos/squat.png')
    frame = cv2.resize(frame, (1280, 720))
    frame = detector.findPose(frame, False)
    lmList = detector.findPosition(frame, False)
    # print (lmList)
    if len(lmList) != 0:
        #landmarks for right arm
        # detector.findAngle(frame, 12, 14, 16)
        #landmarks for left arm
        # detector.findAngle(frame, 11, 13, 15)

        # landmarks for right leg
        angle = detector.findAngle(frame, 24, 26, 28)
        #landmarks for left leg
        # detector.findAngle(frame, 23, 25, 27)

        # if angle is within the range of (210, 310) then convert it to (0, 100) to get the percentage
        percentage = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
        # print(angle, percentage)

        # check for the dumbbell curls
        color = (255, 0, 255)
        if percentage == 100:
            color = (0, 255, 0)
            if direction == 0:
                count += 0.5
                direction = 1
        
        if percentage == 0:
            color = (0, 255, 0)
            if direction == 1:
                count += 0.5
                direction = 0
        
        # print(count)
        # cv2.rectangle(frame, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        # cv2.putText(frame, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

        # draw bar
        cv2.rectangle(frame, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(frame, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(frame, f'{int(percentage)}%', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)


    # to get the FPS of the video
    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime
    cv2.putText(frame, str(int(fps)), (35,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", frame)

    #exit while loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break