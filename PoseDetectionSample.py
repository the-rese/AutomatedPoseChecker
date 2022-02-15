import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions import pose

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture('videos/7.mp4')
prevTime = 0

while True:
    #capture frame by frame
    success, frame = cap.read()

    #function rescale frame is called to downscale the video
    frame = rescale_frame(frame, percent= 30)

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)
    #to display the landmarks in the frame
    if result.pose_landmarks:
        mpDraw.draw_landmarks(frame, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = frame.shape
            print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y *  h)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)



    #to get the FPS of the video
    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime
    cv2.putText(frame, str(int(fps)), (35,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    #to display the captured frame(s)
    cv2.imshow("Image", frame)
    # cv2.waitKey(10)

    #to exit from the while loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#the capture will be released after everything is done
cap.release()
cv2.destroyAllWindows()