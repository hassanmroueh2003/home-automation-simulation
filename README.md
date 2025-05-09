# Home Automation Simulation

Multimodal home automation simulation using Python, integrating face recognition, eye tracking, hand gestures, and voice recognition for assistive control.

## Overview

This project is a Python-based simulation of a multimodal home automation system developed to support individuals with disabilities or elderly users. The system allows control of home appliances using:

- 👁️ **Eye tracking** (blink and gaze direction)
- ✋ **Hand gestures** (via MediaPipe)
- 🎤 **Voice commands** (via SpeechRecognition and Google API)
- 🧑 **Face recognition** (for user authentication)

The system was originally tested on a laptop and later optimized for deployment on a Raspberry Pi with GPIO and PiCamera2.

---

## Technologies Used

- Python 3.x  
- OpenCV  
- dlib  
- face_recognition  
- MediaPipe  
- SpeechRecognition  
- Raspberry Pi (for hardware version)

---

## Usage

Run the main script to start the interface:

```bash
python main.py
You'll be prompted to log in using face recognition. After authentication, use:

E for eye tracking

H for hand gestures

V for voice commands

X to exit

Dependencies
Install Required Python Packages
bash
Copy
Edit
pip install opencv-python dlib face_recognition mediapipe SpeechRecognition numpy
Download Required Model File
Download and place the following file in the root directory:

shape_predictor_68_face_landmarks.dat
→ Used by eyes2.py for facial landmark detection.

Face Recognition Setup
Create an images/ folder

Inside it, create a subfolder named after the user (e.g., images/hassan/)

Add a JPEG image of the user inside that folder (e.g., hassan.jpeg)

Note
This repository contains the simulation version of the system. For full deployment on a Raspberry Pi:

Replace OpenCV camera functions with picamera2

Integrate GPIO logic for:

Relays (fan, light)

LEDs (visual feedback)

Servo motor (curtain control)

License
This project is intended for educational and demonstrational purposes only.
