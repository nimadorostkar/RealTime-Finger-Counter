import cv2
import mediapipe as mp
import time
import os
import hand_tracking_2 as htm
import random


def generate_random_number():
    while True:
        number = random.randint(0, 5555)
        digits = str(number)
        if not any(digit in digits for digit in ['6', '7', '8', '9']):
            return number

random_number = generate_random_number()
print(random_number)
ch=list(str(random_number))
print(ch)
cap=cv2.VideoCapture(0)

#we needthe images so tha whenever we show our hand displaying the number we're asked to perform we show that image
folderPath="images"
myList=os.listdir(folderPath)
print(myList)

#create an overlay list that contain images that will be overlayed on our main image
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime=0


#create a detector
detector=htm.handDetector(min_detection_confidence=0.75)
tipIds=[4,8,12,16,20]
i=0
j=0
start_time=time.time()
while True:
    while i  <len(ch):
        
        success,img=cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img,draw=False)
        #print(lmlist)
        cv2.putText(img,f'number required:{int(ch[i])}',(20,20),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
        

        if len(lmlist)!=0:
            fingers=[]
            #thumb
            if lmlist[tipIds[0]][1]< lmlist[tipIds[0]-1][1]:
                          fingers.append(1)
            else:
                          fingers.append(0)
            #other fingers
            for id in range(1,5):
                #whatever tip id the one we will compare with is the tip with id minus 2 
                if lmlist[tipIds[id]][2]< lmlist[tipIds[id]-2][2]:
                          fingers.append(1)
                else:
                          fingers.append(0)
            #print(fingers)
            
            totalFingers=fingers.count(1)
            
            #print(totalFingers)
        #in the image we give the region of the height and the width
            iw,ih,ic=overlayList[totalFingers-1].shape
            img[0:iw,0:ih]=overlayList[totalFingers-1]
            cv2.putText(img,f'total:{int(totalFingers)}',(400,80),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
            elapsed_time=time.time()-start_time
            if totalFingers!=int(ch[i]) and elapsed_time<8:
                print("process is failed: next number won't be displayed but you still have essays")
                j+=1
            elif totalFingers!=int(ch[i]) and elapsed_time>=8:
                break
            elif totalFingers==int(ch[i]) and elapsed_time>=4:
                i+=1
                elapsed_time=0
                start_time=time.time()
    
        cTime=time.time()
        fps=1/(cTime-pTime)

        #cv2.putText(img,f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
        pTime=cTime
        cv2.imshow("Image",img)
        key = cv2.waitKey(1) & 0xFF
        if key==ord("q"):
            break
    if i==len(ch) :
        print("successful")
        break
    else:
        print("no more essays you failed")
        break

cv2.destroyAllWindows()