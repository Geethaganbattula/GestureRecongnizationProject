import cv2
import numpy as np
import mediapipe as mp
from comtypes import CLSCTX_ALL, cast, POINTER
from math import hypot
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize Audio Control
audio_devices = AudioUtilities.GetSpeakers()
volume_interface = audio_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(volume_interface, POINTER(IAudioEndpointVolume))
min_volume, max_volume, _ = volume_control.GetVolumeRange()  # Get actual volume range

# Initialize Hand Tracking
mp_hands = mp.solutions.hands
hand_tracker = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.8,  # Increased confidence
    min_tracking_confidence=0.8
)
drawing_utils = mp.solutions.drawing_utils

# Start Camera
camera = cv2.VideoCapture(0)

def get_landmark_position(hand_landmarks, landmark_id, img_shape):
    """ Returns (x, y) coordinates of a specific landmark """
    height, width, _ = img_shape
    return int(hand_landmarks.landmark[landmark_id].x * width), int(hand_landmarks.landmark[landmark_id].y * height)

def process_hands(image):
    """ Detect hands, extract key landmarks, and return brightness & volume distances """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hand_tracker.process(image_rgb)

    left_distance = right_distance = None  # Default values

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label

            try:
                thumb_tip = get_landmark_position(hand_landmarks, 4, image.shape)
                index_tip = get_landmark_position(hand_landmarks, 8, image.shape)

                distance = hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

                if label == "Left":
                    left_distance = distance
                else:
                    right_distance = distance

                # Draw Hand Landmarks
                drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            except IndexError:
                pass  # Prevents crashes if landmarks are missing

    return left_distance, right_distance

try:
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)

        # Get brightness & volume distances
        left_distance, right_distance = process_hands(frame)

        # Adjust brightness
        if left_distance:
            brightness = np.interp(left_distance, [50, 200], [0, 100])  # 0 to 100 range
            brightness = np.clip(brightness, 0, 100)  # Ensure it's between 0-100
            sbc.set_brightness(int(brightness))
            cv2.putText(frame, f'Brightness: {int(brightness)}%', (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Adjust volume
        if right_distance:
            volume_percentage = np.interp(right_distance, [50, 200], [0, 100])  # 0 to 100 range
            volume_percentage = np.clip(volume_percentage, 0, 100)  # Ensure it's between 0-100

            # Convert to scalar value (0.0 to 1.0 for Pycaw)
            volume_control.SetMasterVolumeLevelScalar(volume_percentage / 100, None)

            cv2.putText(frame, f'Volume: {int(volume_percentage)}%', (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Show Camera Feed
        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Exit on 'ESC' key
            break

finally:
    camera.release()
    cv2.destroyAllWindows()
