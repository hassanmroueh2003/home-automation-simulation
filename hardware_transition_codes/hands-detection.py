import cv2
import math
import time  # Import the time module for timer functionality
import mediapipe as mp
from picamera2 import Picamera2
import RPi.GPIO as GPIO

# Configure camera resolution (adjust as needed)
resolution = (640, 480)
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for LEDs
led_pin_1 = 25
led_pin_2 = 23
led_pin_3 = 24

# Setup LED pins as outputs
GPIO.setup(led_pin_1, GPIO.OUT)
GPIO.setup(led_pin_2, GPIO.OUT)
GPIO.setup(led_pin_3, GPIO.OUT)


# Function to toggle LED state
def toggle_led(pin):
    GPIO.output(pin, not GPIO.input(pin))


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
# Initialize picamera2 instance
picam2 = Picamera2()

# Configure preview stream
picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": resolution}))

# Start the stream
picam2.start()
# Initialize the video capture object
# cap = cv2.VideoCapture(0)  # Use 0 for the default camera (webcam)

# Initialize drawing variables
draw_color = (0, 255, 0)
prev_x, prev_y = 0, 0

# Initialize command variables
command_texts = {
    5: "Lights ON/OFF",
    0: "no command",
    1: "Fans ON/OFF",
    2: "Extension ON/OFF",
    3: "no command",
    4: "no command"
}

# Initialize confirmation variables
confirmation_time = 5  # Confirmation time in seconds
confirmation_start_time = 0
confirmed_command = None

while True:
    # Capture video from your webcam
    frame = picam2.capture_array()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get hand landmarks as a list
            landmarks = [(int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                         for landmark in hand_landmarks.landmark]

            # Count fingers
            finger_count = 0

            # Thumb (Landmark 4) check
            if landmarks[4][1] < landmarks[3][1]:
                finger_count += 1

            # Four fingers (Landmarks 8, 12, 16, 20) check
            for landmark_id in [8, 12, 16, 20]:
                if landmarks[landmark_id][1] < landmarks[landmark_id - 2][1]:
                    finger_count += 1

            # Display the finger count
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Check for specific hand gestures and confirmation
            if finger_count in command_texts:
                current_time = time.time()
                if confirmed_command == finger_count:
                    if current_time - confirmation_start_time >= confirmation_time:
                        print(command_texts[finger_count])  # Perform the command
                        if finger_count == 5:
                            toggle_led(led_pin_3)
                        elif finger_count == 1:
                            toggle_led(led_pin_1)
                        elif finger_count == 2:
                            toggle_led(led_pin_2)
                        confirmed_command = None  # Reset confirmed command
                else:
                    confirmation_start_time = current_time
                    confirmed_command = finger_count

                # Display the command text
                cv2.putText(frame, command_texts[finger_count], (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the video frame
    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the stream and clean up
GPIO.cleanup()
picam2.stop()
cv2.destroyAllWindows()