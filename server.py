from flask import Flask, render_template, Response, redirect, url_for, jsonify
import cv2
import threading
import mediapipe as mp
import pyautogui
import time
import numpy as np
import util  # Importing custom gesture detection functions
from pynput.mouse import Controller
from screen_brightness_control import set_brightness
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, cast, POINTER

app = Flask(__name__)  # ✅ Fixed

# Mouse Control
mouse_controller = Controller()
screen_w, screen_h = pyautogui.size()

# MediaPipe Hands Model
mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

# Audio Control Setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = interface.QueryInterface(IAudioEndpointVolume)

# Global Variables
video_capture = None
tracking = False
last_click_time = 0
click_cooldown = 0.3  # Cooldown for clicks

# **✅ Routes Setup**  
@app.route('/')
def home():
    return render_template('about.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/g_page')
def g_page():
    return render_template('g.html')

@app.route('/gesture_control')
def gesture_control():
    return render_template('index.html')

# **🎥 Video Processing & Gesture Recognition**
def generate_frames():
    global video_capture, last_click_time, tracking

    video_capture = cv2.VideoCapture(0)

    while tracking and video_capture.isOpened():
        success, frame = video_capture.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_data = hand_detector.process(frame_rgb)

        if hand_data.multi_hand_landmarks:
            for hand_landmarks in hand_data.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                
                cursor_x = int(landmarks[8][0] * screen_w)
                cursor_y = int(landmarks[8][1] * screen_h)

                if util.detect_cursor_move(landmarks):
                    pyautogui.moveTo(cursor_x, cursor_y)

                current_time = time.time()
                
                if util.detect_left_click(landmarks):
                    if current_time - last_click_time > click_cooldown:
                        pyautogui.click()
                        last_click_time = current_time

                if util.detect_right_click(landmarks):
                    if current_time - last_click_time > click_cooldown:
                        pyautogui.rightClick()
                        last_click_time = current_time

                if util.detect_double_click(landmarks):
                    if current_time - last_click_time > click_cooldown:
                        pyautogui.doubleClick()
                        last_click_time = current_time

                if util.detect_screenshot_gesture(landmarks):
                    screenshot_path = "screenshot.png"
                    pyautogui.screenshot(screenshot_path)
                    print(f"Screenshot saved at: {screenshot_path}")

                volume_level = util.detect_volume_control(landmarks)
                volume_control.SetMasterVolumeLevelScalar(volume_level / 100, None)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    if video_capture:
        video_capture.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start')
def start():
    global tracking
    if not tracking:
        tracking = True
        print("✅ Gesture Tracking Started")
    return jsonify(status='started')

@app.route('/stop')
def stop():
    global tracking, video_capture
    tracking = False
    if video_capture:
        video_capture.release()
    print("🔴 Gesture Tracking Stopped")
    return jsonify(status='stopped')

@app.route('/go_to_g_page')
def go_to_g_page():
    return redirect(url_for('g_page'))

@app.route('/go_to_gesture_control')
def go_to_gesture_control():
    return redirect(url_for('about'))  # ✅ Redirects to index.html

# **🚀 Start Flask Server**
if __name__ == '__main__':  # ✅ Fixed
    app.run(debug=True)
