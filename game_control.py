import cv2
import pyautogui
import time
import hand_track as htm  # Make sure the filename is hand_track.py

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Initialize Hand Detector
detector = htm.HandDetector(detectionCon=0.8)

# Cooldown between commands
cooldown = 1.0  # seconds
last_action_time = time.time()

# Intro Screen
print("Starting Hand Game Controller...")
time.sleep(2)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    totalFingers = 0  # Default value to avoid NameError

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[4][1] > lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers (Index, Middle, Ring, Pinky)
        for id in [8, 12, 16, 20]:
            if lmList[id][2] < lmList[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        current_time = time.time()

        if current_time - last_action_time > cooldown:
            if totalFingers == 1:
                pyautogui.press('up')
                print("Jump triggered")
                last_action_time = current_time

            elif totalFingers == 2:
                pyautogui.press('right')
                print("Move right triggered")
                last_action_time = current_time

            elif totalFingers == 3:
                pyautogui.press('left')
                print("Move left triggered")
                last_action_time = current_time

            elif totalFingers == 4:
                pyautogui.press('down')
                print("Slide down triggered")
                last_action_time = current_time

            elif totalFingers == 5:
                pyautogui.press('space')
                print("Pause triggered")
                last_action_time = current_time

    # Display number of fingers detected
    cv2.putText(img, f'Fingers: {totalFingers}', (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Show camera feed
    cv2.imshow("Hand Game Controller", img)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
