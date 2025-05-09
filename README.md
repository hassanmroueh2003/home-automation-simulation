# Home Automation Simulation

**Multimodal home automation simulation using Python**, integrating face recognition, eye tracking, hand gestures, and voice recognition for assistive control.

---

## 🧩 Overview

This project is a Python-based simulation of a multimodal home automation system developed to support individuals with disabilities or elderly users. The system allows control of home appliances using:

* 👁️ **Eye tracking** (blink and gaze direction)
* ✋ **Hand gestures** (via MediaPipe)
* 🎤 **Voice commands** (via SpeechRecognition and Google API)
* 🧑 **Face recognition** (for user authentication)

The system was originally tested on a laptop and later optimized for deployment on a Raspberry Pi using GPIO and PiCamera2.

---

## ⚙️ Technologies Used

* Python 3.x
* OpenCV
* dlib
* face\_recognition
* MediaPipe
* SpeechRecognition
* Raspberry Pi (for hardware deployment)

---

## 🚀 Usage

To start the system, run the main script:

```bash
python main.py
```

You’ll be prompted to log in using face recognition. After authentication, use the following keys:

* `E` → Eye tracking
* `H` → Hand gestures
* `V` → Voice commands
* `X` → Exit the program

---

## 📦 Dependencies

### Install Required Python Packages

```bash
pip install opencv-python dlib face_recognition mediapipe SpeechRecognition numpy
```

### Download Required Model File

Download and place the following file in the root directory:

* `shape_predictor_68_face_landmarks.dat`
  → Used by `eyes2.py` for facial landmark detection.

📥 [Download shape\_predictor\_68\_face\_landmarks.dat](https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat)

---

## 🧑‍🦰 Face Recognition Setup

1. Create a folder named `images/`

2. Inside it, create a subfolder named after the user, e.g.:

   ```
   images/hassan/
   ```

3. Add a JPEG image of the user inside that folder:

   ```
   images/hassan/hassan.jpeg
   ```

---

## 📝 Notes

This repository contains a **simulation version** of the system. For **Raspberry Pi deployment**:

* Replace OpenCV camera functions with **PiCamera2**
* Integrate **GPIO logic** for:

  * Relays (e.g., fan, light)
  * LEDs (visual feedback)
  * Servo motors (e.g., curtain control)

---

## 📄 License

This project is intended for **educational and demonstrational purposes only**.
