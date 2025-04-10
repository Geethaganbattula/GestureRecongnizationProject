# 🖐️ Gesture-Based Computer Control System

This project is a real-time hand gesture recognition system built using OpenCV, MediaPipe, and PyAutoGUI. It allows users to control their computer (mouse, volume, brightness, etc.) using only hand gestures captured via webcam.

---

## 🚀 Features

- 📹 Real-time hand tracking using MediaPipe
- 🖱️ Mouse cursor movement with index finger
- 👆 Left click and drag using finger gestures
- 🔉 Volume control using finger distance
- 🌞 Screen brightness adjustment with thumb-index gestures
- 🔒 Modular structure for adding more gestures

---

## 🛠️ Tech Stack

- Python 3.8+
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://google.github.io/mediapipe/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
- [screen_brightness_control](https://pypi.org/project/screen-brightness-control/)
- [pycaw](https://github.com/AndreMiras/pycaw)

---

## 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/gesture-control-system.git
    cd gesture-control-system
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the project**:
    ```bash
    python main.py
    ```

---

## ✋ Assigned Finger Gestures

| Gesture                     | Action                  |
|----------------------------|-------------------------|
| Index finger up            | Move mouse cursor       |
| Index + Middle finger up   | Left click              |
| Thumb + Index close        | Volume or brightness    |
| All fingers up             | Neutral (No action)     |

> You can customize gestures in the code based on `landmark` positions.

---

## 📁 Folder Structure

