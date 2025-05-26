import cv2
import mediapipe as mp
import time
import pyautogui

def detectGesture(fingers):
    """
    Returns a string and triggers a keypress based on the finger pattern.
    """
    if fingers == [0, 1, 0, 0, 0]:
        pyautogui.press('up')  # Jump
        return "Jump"
    elif fingers == [1, 1, 0, 0, 0]:
        pyautogui.press('down')  # Roll
        return "Roll"
    elif fingers == [0, 1, 1, 0, 0]:
        pyautogui.press('right')  # Move Right
        return "Move Right"
    elif fingers == [1,0, 0, 0, 0]:
        pyautogui.press('left')  # Move Left
        return "Move Left"
    elif fingers == [1, 1, 1, 1, 1]:
        pyautogui.press('space')  # Hoverboard
        return "Hoverboard"
    else:
        return "No Action"

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    from Gesture_Recognition import handDetector
    detector = handDetector()
    gesture = ""
    lastGestureTime = 0  # To track time between gestures
    gestureCooldown = 0.5  # Cooldown in seconds

    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    while True:
        success, img = cap.read()
        if not success or img is None:
            print("❌ Failed to grab frame")
            continue

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        currentTime = time.time()
        if len(lmList) != 0 and (currentTime - lastGestureTime) > gestureCooldown:
            try:
                fingers = detector.fingersUp()
                gesture = detectGesture(fingers)
                print("Gesture:", gesture)
                lastGestureTime = currentTime  # Reset cooldown
            except Exception as e:
                print("⚠️ Error in gesture detection:", e)
                gesture = "Error"

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
        pTime = cTime

        # Display info
        cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f'Gesture: {gesture}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, "Press 'q' to quit", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 255), 2)

        cv2.imshow("Hand Gesture Recognition", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
