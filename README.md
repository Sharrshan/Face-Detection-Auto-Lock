# Automatic Screen Lock using Face Detection

This is a simple security tool written in Python that uses a webcam to detect a user's presence. If a face is not detected for a specified period, the script automatically locks the computer.

## Features
- Real-time face detection using the webcam.
- Configurable delay before locking the screen.
- Cross-platform support for Windows, macOS, and Linux.

## Technologies Used
- **Language:** Python
- **Libraries:**
  - OpenCV (`opencv-python`): For capturing video and performing face detection.
  - OS & Platform: To run system-specific screen lock commands.

## How to Run It
1.  Ensure you have Python and `opencv-python` installed.
2.  Download the `main.py` and `haarcascade_frontalface_default.xml` files.
3.  Place both files in the same folder.
4.  Run the script from your terminal: `python main.py`

## What I Learned
- Basic computer vision principles.
- How to use the OpenCV library to access a webcam and process image frames.
- Implementing logic based on real-time data.
- Interacting with the operating system using Python.
