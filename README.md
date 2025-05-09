# home-automation-simulation
Multimodal home automation simulation using Python, integrating face recognition, eye tracking, hand gestures, and voice recognition for assistive control.
# Home Automation Simulation

This project is a Python-based simulation of a multimodal home automation system built for assistive technology. It supports:

- Eye tracking (for gaze direction and blinking)
- Hand gesture recognition (via MediaPipe)
- Voice command control (via SpeechRecognition)
- Face recognition for authentication

Originally developed for laptop simulation, later optimized for Raspberry Pi with GPIO and PiCamera2.

## Technologies
- Python
- OpenCV
- dlib
- MediaPipe
- SpeechRecognition
- Raspberry Pi (for full deployment)

## Usage
Run `main.py` to start the interface. You'll be prompted to log in using face recognition, then choose between hand, eye, or voice control.
