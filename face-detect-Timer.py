import cv2
from simple_facerec import SimpleFacerec
import time

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/hassan")
# Load Camera
cap = cv2.VideoCapture(0)

# Define the duration of the timer in seconds
duration = 5  # 5 seconds

# Initialize timer variables
timer_start = time.time()
hassan_detected = False

while True:
    ret, frame = cap.read()
    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        if name == "hassan":
            hassan_detected = True

    # Check if 5 seconds have passed and "hassan" is still detected
    if time.time() - timer_start >= duration and hassan_detected:
        print("hassan is here")
        # Reset timer
        timer_start = time.time()
        hassan_detected = False

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
