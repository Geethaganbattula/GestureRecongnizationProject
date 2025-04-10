# Gesture Based Computer Control

The Gesture-based Computer Control project enables users to control their computers using hand gestures captured through a webcam. The project allows for gesture-based control of system volume, brightness, and mouse actions such as click, drag,taking screenshots and cursor movements. This tool provides a hands-free way to interact with the computer, making it highly accessible and user-friendly.


## Demo

https://youtu.be/ezjAREzzohM


## Features

- Volume Control: Adjust system volume using Right Hand fingre .
- Brightness Control: Control system brightness through Left hand fingre.
- Virtual Mouse: Using One hand Gesture Left Click, Right Click, Double Click,   Dragging, taking Screenshot
- Real-time Gesture Recognition: Detect and process hand gestures in real time via webcam input.
- Seamless Integration: Works without additional hardware, requiring only a webcam.


## Project Structure
- Drag_Click_screenshot_cursor.ipynb: Jupyter notebook for handling mouse controls (click, drag, cursor movement,screenshot) using hand gestures.
- Volume_Brightness.ipynb: Jupyter notebook for managing system volume and brightness adjustments using gestures.
- util.py: Python file containing utility functions for hand gesture detection and recognition.
## Tech Stack
**IDE**
- Jupyter Notebook: Interactive environment for developing and running the gesture control features.
**Backend**
- Python: Main language used to create gesture recognition and control logic.
- OpenCV: Library used for webcam input and frame processing.
- Mediapipe: Google's real-time hand gesture recognition library.
- PyAutoGUI: Used for controlling system functions (mouse, volume, brightness) programmatically.
- screen_brightness_control: installed it for controlling brightness
- pycaw: For Audio control
- Numpy: Used for numerical computations and array manipulation.

## Setup
**Prerequisites**
- Python 3.6 or higher
- Jupyter Notebook or any Python based IDE
- Webcam for capturing hand gestures


**Installation**

Clone the repository and set up the environment:
```bash
  git clone https://github.com/your-repo/gesture-based-computer-control.git
  cd gesture-based-computer-control

```
Install the required  python dependencies for Volume_Brighness.ipynb:  

```bash
  pip install cv
  pip install numpy
  pip install mediapipe
  pip install screen_brightness_control
  pip install pycaw
```
Install the required  python dependencies for Drag_Click_screenshot_cursor.ipynb:

```bash
  pip install pyautogui
  pip install pynput
```
## Authors

- [@SHOVIK CHAKRABORTY](https://github.com/cshovik)


## License

[MIT](https://github.com/cshovik/Gesture-Based-Computer-Control?tab=MIT-1-ov-file#readme)

## Screenshot:
![screenshot_619](https://github.com/user-attachments/assets/8d0b15f4-3b46-437e-a705-56d1ba11cde9)



