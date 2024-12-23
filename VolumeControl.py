import cv2
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTracking as htm  # Ensure this module is in the same directory

# Camera and Window Setup
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)  # Use 0 for default camera
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height

# Initialize Variables
pTime = 0  # Previous time for FPS calculation
detector = htm.handDetector(detectionCon=0.7)  # Hand detector with 0.7 confidence

# Pycaw Audio Initialization
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()  # Get volume range
minVol = volRange[0]  # Minimum volume level
maxVol = volRange[1]  # Maximum volume level
vol = 0
volBar = 400
volPer = 0

while True:
    # Read Camera Input
    success, img = cap.read()
    if not success:
        print("Failed to capture image.")
        break

    # Detect Hands
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)  # Get landmark positions

    if len(lmList) != 0:
        # Extract Coordinates for Thumb and Index Finger
        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip
        x2, y2 = lmList[8][1], lmList[8][2]  # Index tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Center point

        # Draw Indicators
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Calculate Distance Between Thumb and Index Finger
        length = math.hypot(x2 - x1, y2 - y1)

        # Map Distance to Volume Range
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        # Set Volume
        volume.SetMasterVolumeLevel(vol, None)

        # Visual Feedback for Close Fingers
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Draw Volume Bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # Calculate and Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # Show Image
    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
        break

# Release Camera and Close Windows
cap.release()
cv2.destroyAllWindows()