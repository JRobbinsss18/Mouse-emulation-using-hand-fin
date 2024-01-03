import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Initialize MediaPipe drawing module
mp_drawing = mp.solutions.drawing_utils

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Variables for smoothed movement
smoothed_tip = np.array([0, 0], dtype=np.float32)
smoothing_factor = 0.2  # Adjust for smoother movement
is_dragging = False  # Flag for drag action

def is_thumb_index_touching(index_tip, thumb_tip):
    # Check if thumb and index fingertips are close enough
    distance = np.linalg.norm([index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y, index_tip.z - thumb_tip.z])
    return distance < 0.05  # Adjust this threshold as needed

def is_fist(hand_landmarks):
    # Check if all fingers are closed to form a fist
    fingertips = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
                  mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
                  mp_hands.HandLandmark.PINKY_TIP]
    for fingertip in fingertips:
        if hand_landmarks.landmark[fingertip].y < hand_landmarks.landmark[fingertip - 2].y:
            return False
    return True

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Flip image for a selfie-view display
    image = cv2.flip(image, 1)

    # Convert image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    results = hands.process(image)

    # Draw hand landmarks
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmarks of index finger tip and thumb tip
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert index tip coordinates to screen resolution
            screen_w, screen_h = pyautogui.size()
            x, y = int(index_tip.x * screen_w), int(index_tip.y * screen_h)  # Correct Y-axis calculation

            # Smooth the movement
            smoothed_tip = smoothed_tip * (1 - smoothing_factor) + np.array([x, y]) * smoothing_factor

            # Move mouse cursor
            pyautogui.moveTo(smoothed_tip[0], smoothed_tip[1])

            # Check if thumb and index finger are touching
            currently_touching = is_thumb_index_touching(index_tip, thumb_tip)

            # Handle click and drag
            if currently_touching and not is_dragging:
                pyautogui.mouseDown()
                is_dragging = True
            elif not currently_touching and is_dragging:
                pyautogui.mouseUp()
                is_dragging = False

            # Check for fist gesture
            if is_fist(hand_landmarks):
                wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                if wrist_x < 0.5:  # Fist on left side of the screen
                    pyautogui.press('left')
                else:  # Fist on right side of the screen
                    pyautogui.press('right')

    # Display the image
    cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
