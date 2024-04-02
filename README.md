

# HandBot

HandBot was my first project in computer vision, utilizing the advanced capabilities of computer vision and machine learning, this program interprets specific hand gestures captured via a webcam and translates them into corresponding computer commands. This program leverages the powerful libraries of OpenCV and MediaPipe for real-time hand detection and tracking, along with PyAutoGUI for controlling the mouse and keyboard, providing a seamless and intuitive user experience.

# Installation

To use HandBot, you must first download some libraries as well as optionally set up a virtual environment.

*pip install opencv-python mediapipe pyautogui numpy*

# Usage

To actually run HandBot, run:

*python HandBot.py*


# Hand mouse controls

*
- Mouse is the tip of your index, so for best use, make a fist with your middle ring and pinky so it can't confuse your index with any other finger, even though in most cases it wont.
- Tapping or holding your index & thumb emulates left mouse click (selection).
- Making a fist on the left side of the screen emulates left arrow click (built for slideshow presentations primarily)
- Making a fist on the right side of the screen emulates left arrow click (built for slideshow presentations primarily)

For the left/right features, timing of when left/right registers changes based on framerate of your webcam, holding the pose will press it multiple times. getting the timing right to only press left/right once is fairly easy once you test it out.*
