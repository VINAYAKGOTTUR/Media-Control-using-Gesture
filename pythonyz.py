import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_action_time = 0
delay = 1   # seconds delay between actions


def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            total = count_fingers(hand_landmarks)

            current_time = time.time()

            if current_time - last_action_time > delay:

                # ----- Gesture Controls -----
                if total == 1:
                    pyautogui.press("playpause")
                    action = "Play / Pause"

                elif total == 2:
                    pyautogui.press("volumeup")
                    action = "Volume Up"

                elif total == 3:
                    pyautogui.press("volumedown")
                    action = "Volume Down"

                elif total == 4:
                    pyautogui.press("nexttrack")
                    action = "Next Track"

                elif total == 5:
                    pyautogui.press("prevtrack")
                    action = "Previous Track"

                elif total == 0:
                    pyautogui.press("volumemute")
                    action = "Mute"

                else:
                    action = ""

                if action:
                    print(action)
                    last_action_time = current_time

            cv2.putText(img, f"Fingers: {total}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Gesture Media Controller", img)

    key = cv2.waitKey(1)

    # Press 'q' to exit
    if key == ord('q'):
        break

    # Press 's' for screenshot
    if key == ord('s'):
        pyautogui.screenshot("gesture_screenshot.png")

cap.release()
cv2.destroyAllWindows()