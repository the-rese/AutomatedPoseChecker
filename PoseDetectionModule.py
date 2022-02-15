import cv2
import mediapipe as mp
import time
import math

from mediapipe.python.solutions import pose

# Here are the new things added in the code:
# 1. added new function called find Angle
# 2. draw is updated
# 3. lmList is a global data for the PoseDetector class

class PoseDetector():

    #initial function for the class pose detector
    #initializes the object needed for pose detection
    def __init__(self, static_img_mode = False, upper_body_only = False, smooth_landmarks = True, min_detection_con = 0.5, min_tracking_con = 0.5):
        self.static_img_mode = static_img_mode
        self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_con = min_detection_con
        self.min_tracking_con = min_tracking_con

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_img_mode, self.upper_body_only, self.smooth_landmarks, self.min_detection_con, self.min_tracking_con)
        
    #function for finding the landmarks
    def findPose(self, frame, draw = True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)
        
        #to display the landmarks in the frame
        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame, self.result.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return frame

    #to get the Position of the landmarks
    def findPosition(self, frame, draw = True):
        #create a list for the landmarks
        self.lmList = []

        if self.result.pose_landmarks:
            for id, lm in enumerate(self.result.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y *  h)

                #append only the id, x and y values
                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    #function for finding the angle between 3 points
    def findAngle(self, frame, p1, p2, p3, draw = True):

        # getting the landmarks of each points
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        #calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        
        if draw:
            cv2.line(frame, (x1,y1), (x2,y2), (255,255,255), 3)
            cv2.line(frame, (x3,y3), (x2,y2), (255,255,255), 3)
            cv2.circle(frame, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(frame, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(frame, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.putText(frame, str(int(angle)),(x2 - 20, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        return angle

# this is only used for testing
# def rescale_frame(frame, percent=75):
#     width = int(frame.shape[1] * percent/ 100)
#     height = int(frame.shape[0] * percent/ 100)
#     dim = (width, height)
#     return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)    

# def main():
#     cap = cv2.VideoCapture('videos/1.mp4')
#     prevTime = 0
#     detector = PoseDetector()

#     while True:
#         #capture frame by frame
#         success, frame = cap.read()

#         #function rescale frame is called to downscale the video
#         frame = rescale_frame(frame, percent= 30)

#         frame = detector.findPose(frame)
#         lmList = detector.findPosition(frame)
#         print(lmList)

#         #to get the FPS of the video
#         currTime = time.time()
#         fps = 1/(currTime-prevTime)
#         prevTime = currTime
#         cv2.putText(frame, str(int(fps)), (35,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

#         #to display the captured frame(s)
#         cv2.imshow("Image", frame)
        
#         #to exit from the while loop
#         if cv2.waitKey(20) & 0xFF == ord('q'):
#             break

#     #the capture will be released after everything is done
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()