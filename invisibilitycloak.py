import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

time.sleep(2)


background = None
for i in range(30):
    ret, frame = cap.read()
    if ret:
        background = frame
    else:
        print("Error: Could not capture background frame.")
        cap.release()
        exit()
background = np.flip(background, axis=1)  


lower_green = np.array([0, 0, 200])  
upper_green = np.array([179, 30, 255])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = np.flip(frame, axis=1)  

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_green, upper_green)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask_inv = cv2.bitwise_not(mask)

    frame_fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    background_fg = cv2.bitwise_and(background, background, mask=mask)
    result = cv2.add(frame_fg, background_fg)

    cv2.imshow("Invisibility Cloak", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()