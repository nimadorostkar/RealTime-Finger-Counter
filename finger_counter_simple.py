import cv2
import hand_tracking_2 as htm

cap = cv2.VideoCapture(0)
detector = htm.handDetector(min_detection_confidence=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        fingers = []
        # Thumb
        fingers.append(1 if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1] else 0)
        # Other fingers
        for id in range(1, 5):
            fingers.append(1 if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2] else 0)

        totalFingers = fingers.count(1)
        cv2.putText(img, f'Fingers: {totalFingers}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()