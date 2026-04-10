import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.7, maxHands=2)
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    # Reset steering keys
    pyautogui.keyUp("left")
    pyautogui.keyUp("right")

    if hands:
        for hand in hands:
            handType = hand["type"]
            fingers = detector.fingersUp(hand)
            totalFingers = fingers.count(1)

            cv2.putText(img, f'{handType}: {totalFingers}',
                        (50, 50 if handType=="Left" else 100),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

            # ✋ LEFT HAND → ACCELERATE / BRAKE
            if handType == "Left":
                if totalFingers == 5:
                    pyautogui.keyUp("down")   # stop reverse
                    pyautogui.keyDown("up")   # accelerate

                elif totalFingers == 0:
                    pyautogui.keyUp("up")     # brake

            # 🤚 RIGHT HAND → STEERING + REVERSE
            elif handType == "Right":

                if totalFingers == 1:
                    pyautogui.keyDown("left")

                elif totalFingers == 2:
                    pyautogui.keyDown("right")

                elif totalFingers == 5:
                    pyautogui.keyUp("up")     # stop forward
                    pyautogui.keyDown("down") # reverse

                else:
                    pyautogui.keyUp("down")   # stop reverse if not 5

    cv2.imshow("Driving Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()