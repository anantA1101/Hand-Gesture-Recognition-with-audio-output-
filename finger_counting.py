import cv2
import time
import os
import HandTrackingModule as htm
from playsound import playsound
import threading

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = r"D:\DEEP LEARNING CODES\HAND_TRACKING\finger_pics"
myList = os.listdir(folderPath)
overlayList = []


for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)


pTime = 0
cTime = 0
detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

audio_list=[]
totalFingers= 0
break_other_loop=False

def play_audio():
    global audio_list
    global totalFingers,break_other_loop
    while True:
        audio_list.append(totalFingers)
        #print(audio_list)
        if len(audio_list)>5:
            if audio_list[-1] != audio_list[-2]:
                    playsound(r'D:\DEEP LEARNING CODES\HAND_TRACKING\Audio/'+str(totalFingers)+'.mp3')
                    
        if break_other_loop:
            break
    
def Always_running():
    global totalFingers
    global cTime, pTime,tipIds, break_other_loop
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)

        if len(lmList) != 0:
            fingers = []

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            totalFingers = fingers.count(1)
    

            h, w, c = overlayList[totalFingers - 1].shape
            img[0:h, 0:w] = overlayList[totalFingers - 1]

            cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,10, (255, 0, 0), 25)
            #cv2.line(img, (320,0),(320,640),(255,0,0),2)



            

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        
        key=cv2.waitKey(1)
        if key==27:
            break_other_loop = True
            break
    cv2.destroyAllWindows()

thread1 = threading.Thread(target=Always_running)
thread1.start()

thread2 = threading.Thread(target=play_audio)
thread2.start()