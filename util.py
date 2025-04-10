import numpy as np
import pyautogui
import time
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, cast, POINTER
from math import hypot
from collections import deque  # For smoothing

# 🎯 **Initialize Volume Control**
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))
min_volume, max_volume, _ = volume_control.GetVolumeRange()

# 🔹 **Screen Size**
screen_w, screen_h = pyautogui.size()

# 🔹 **Click Timing Variables**
click_cooldown = 0.3
last_click_time = 0

# 🔹 **Smoothing Variables**
smoothing_window = 5
volume_history = deque(maxlen=smoothing_window)
brightness_history = deque(maxlen=smoothing_window)

def get_distance(point1, point2):
    """Calculate Euclidean distance between two points (scaled for screen size)."""
    x1, y1 = int(point1[0] * screen_w), int(point1[1] * screen_h)
    x2, y2 = int(point2[0] * screen_w), int(point2[1] * screen_h)
    return hypot(x2 - x1, y2 - y1)

# 🎯 **Detect Volume Control (Right Hand)**
def detect_volume_control(landmarks):
    """Controls volume using the right hand (thumb-index distance)."""
    try:
        distance = get_distance(landmarks[4], landmarks[8])
        min_dist, max_dist = 30, max(get_distance(landmarks[0], landmarks[5]), 200)
        volume = np.clip(np.interp(distance, [min_dist, max_dist], [0, 100]), 0, 100)
        
        volume_history.append(volume)
        smoothed_volume = int(np.mean(volume_history))

        volume_control.SetMasterVolumeLevelScalar(smoothed_volume / 100, None)
        return smoothed_volume
    except IndexError:
        return None

# 🎯 **Detect Brightness Control (Left Hand)**
def detect_brightness_control(landmarks):
    """Controls brightness using the left hand (thumb-index distance)."""
    try:
        distance = get_distance(landmarks[4], landmarks[8])
        min_dist, max_dist = 30, max(get_distance(landmarks[0], landmarks[5]), 200)
        brightness = np.clip(np.interp(distance, [min_dist, max_dist], [0, 100]), 0, 100)
        
        brightness_history.append(brightness)
        smoothed_brightness = int(np.mean(brightness_history))

        sbc.set_brightness(smoothed_brightness)
        return smoothed_brightness
    except IndexError:
        return None

# 🎯 **Detect Cursor Movement (Both Hands)**
def detect_cursor_move(landmarks):
    """Moves the cursor if the index finger is extended."""
    index_tip = landmarks[8]
    index_pip = landmarks[6]
    return index_tip[1] < index_pip[1]

# 🎯 **Detect Left Click Gesture (Both Hands)**
def detect_left_click(landmarks):
    """Detects a left-click gesture."""
    return landmarks[8][1] > landmarks[6][1] and landmarks[12][1] > landmarks[10][1]

# 🎯 **Detect Right Click Gesture (Both Hands)**
def detect_right_click(landmarks):
    """Detects a right-click gesture."""
    return landmarks[12][1] > landmarks[10][1] and landmarks[8][1] < landmarks[6][1]

# 🎯 **Detect Double Click Gesture (Both Hands)**
def detect_double_click(landmarks):
    """Detects a double-click gesture with cooldown handling."""
    global last_click_time
    if detect_left_click(landmarks):
        current_time = time.time()
        if current_time - last_click_time < 0.5:
            last_click_time = 0
            return True
        last_click_time = current_time
    return False

# 🎯 **Detect Screenshot Gesture (Both Hands)**
def detect_screenshot_gesture(landmarks):
    """Detects a screenshot gesture when all fingers are extended."""
    return all(landmarks[i][1] < landmarks[i - 2][1] for i in range(5, 21, 4))
