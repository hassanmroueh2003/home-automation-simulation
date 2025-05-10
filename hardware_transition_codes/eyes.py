import cv2  # OpenCV for computer vision tasks
import numpy as np  # NumPy for numerical operations
import dlib  # dlib for face detection and facial landmark detection
from math import hypot  # Importing hypot function from math module
from picamera2 import Picamera2
import time  # Import the time module for timer functionality
import RPi.GPIO as GPIO

# Initializing video capture from default camera (index 0)
# cap = cv2.VideoCapture(0)
# resolution = (640, 480)
# picam2 = Picamera2()
# Configure camera resolution (adjust as needed)
resolution = (640, 480)
# Configure preview stream
# picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": resolution}))
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


# Start the stream
# picam2.start()
# Initializing face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# Function to calculate midpoint between two points
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


# Setting font for text overlay
font = cv2.FONT_HERSHEY_SIMPLEX


# Function to calculate blinking ratio of an eye
def get_blinking_ratio(eye_points, facial_landmarks):
    # Extracting coordinates of eye landmarks
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)

    # Calculating center points of top and bottom eye boundaries

    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    # Calculating lengths of horizontal and vertical lines

    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    # Calculating blinking ratio
    ratio = hor_line_length / ver_line_length
    return ratio


# Function to calculate gaze ratio of an eye

def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)
                                ], np.int32)

    #         print(left_eye_region)
    #         cv2.polylines(frame, [left_eye_region] , True, (0,0,255),2)

    # Creating a mask for the left eye region
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)

    # Drawing a polygonal curve (polyline) representing the outline of the left eye region on the mask image
    # cv2.polylines() draws the polyline on the mask image
    # Arguments:
    #   - mask: the image on which the polyline will be drawn
    #   - [left_eye_region]: a list containing the points that define the polyline, representing the left eye region
    #   - True: indicates that the polyline is closed, meaning the last point is connected to the first point
    #   - 255: the color of the polyline, white in this case (since grayscale, white = 255)
    #   - 2: the thickness of the polyline

    cv2.polylines(mask, [left_eye_region], True, 255, 2)

    # cv2.fillPoly() fills the interior of the polygon with the specified color
    # Arguments:
    #   - mask: the image on which the polygon will be filled
    #   - [left_eye_region]: a list containing the points that define the polygon, representing the left eye region
    #   - 255: the color used to fill the polygon, white in this case (since grayscale, white = 255)

    cv2.fillPoly(mask, [left_eye_region], 255)

    # Applying the mask to extract the left eye
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    #         eye = frame[min_y:max_y,min_x:max_x]
    #         gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
    #         _,threshold_eye = cv2.threshold(gray_eye, 40, 255, cv2.THRESH_BINARY)

    # Thresholding the eye to separate the white parts
    # Extracting the region of interest (ROI) from the 'eye' image, which corresponds to the gray-scale image of the left eye
    # Using array slicing to select the region bounded by the coordinates (min_x, min_y) and (max_x, max_y)
    gray_eye = eye[min_y:max_y, min_x:max_x]

    # Applying a binary threshold to the gray-scale image of the left eye to segment it
    # cv2.threshold() is used to perform thresholding
    # Arguments:
    #   - gray_eye: the input image to be thresholded
    #   - 40: the threshold value, pixels with intensity values below this threshold will be set to 0 (black)
    #   - 255: the maximum value that intensity pixels can be set to if they exceed the threshold (white)
    #   - cv2.THRESH_BINARY: specifies the type of thresholding to be applied, converting pixels below the threshold to 0 and above to 255

    _, threshold_eye = cv2.threshold(gray_eye, 40, 255, cv2.THRESH_BINARY)

    # Obtaining the height and width of the thresholded eye image
    # threshold_eye.shape returns a tuple containing the dimensions (height, width, channels) of the image
    # Since the image is grayscale, there is only one channel, so threshold_height and threshold_width represent the dimensions

    threshold_height, threshold_width = threshold_eye.shape

    # Calculating white area on the left and right sides of the eye

    left_side_threshold = threshold_eye[0:threshold_height, 0:int(threshold_width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0:threshold_height, int(threshold_width / 2):threshold_width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    # Calculating gaze ratio based on white areas

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white

    return gaze_ratio


# Main loop for video processing
# Initialize command variables
command_texts = {

    0: "lights ON/OFF",
    1: "FANS ON/OFF",
    2: "no command",
    3: "Emergency call"
}

# Initialize confirmation variables
confirmation_time = 5  # Confirmation time in seconds
confirmation_start_time = 0
confirmed_command = None
i = -1
picam2 = Picamera2()

# Configure preview stream
picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": resolution}))

# Start the stream
picam2.start()

while (True):
    # _, frame = cap.read() # Reading a frame from the video capture
    new_frame = np.zeros((500, 500, 3), np.uint8)  # Creating a blank frame for additional visualizations
    # Capture frame from Picamera2
    # Capture video from your webcam
    frame = picam2.capture_array()
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert to grayscale
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)
    # Capture frame as a NumPy array using picamera2

    # frame = picam2.capture_array()

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converting the frame to grayscale

    faces = detector(gray)  # Detecting faces in the grayscale frame
    for face in faces:

        #         face detection
        #         x,y = face.left(),face.top()
        #         x1,y1 = face.right(),face.bottom()
        #         cv2.rectangle(frame, (x,y),(x1,y1),(0,255,0),2)
        # Calculating blinking ratio for both eyes
        landmarks = predictor(gray, face)  # Predicting facial landmarks for the detected face
        #         print(landmarks.part(36)) # Position of point 36 of face landmarks
        #         x = landmarks.part(36).x
        #         y = landmarks.part(36).y
        #         cv2.circle(frame, (x,y),2,(0,0,255),2)

        #         Detect Blinking

        # Detecting gaze direction

        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)

        # Calculating the average blinking ratio by summing the ratios of the left and right eyes and dividing by 2
        # The blinking ratio indicates the extent of eyelid closure, with higher values indicating more closed eyelids

        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        # Overlaying text based on blinking and gaze ratios

        if (blinking_ratio > 4.95):
            cv2.putText(frame, "lights ON/OFF", (50, 150), font, 3, (255, 0, 0))
            i = 0
        else:
            # Three directions covered - Left side, Right side and Center
            # Gaze Detection
            # Calculating the gaze ratio for the left eye by calling the get_gaze_ratio function
            # The function takes as input the indices of the landmarks corresponding to the left eye and the facial landmarks
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)

            # Calculating the gaze ratio for the right eye by calling the get_gaze_ratio function
            # The function takes as input the indices of the landmarks corresponding to the right eye and the facial landmarks

            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)

            # Calculating the average gaze ratio by summing the ratios of the left and right eyes and dividing by 2
            # The gaze ratio indicates the direction of the gaze, with higher values indicating the gaze towards the left
            # and lower values indicating the gaze towards the right

            gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye) / 2

            # Printing the gaze ratio for debugging or monitoring purposes
            # print(gaze_ratio)

            #         cv2.putText(frame, str(left_side_white), (50,100), font, 2, (0,0,255), 3)
            #         cv2.putText(frame, str(right_side_white), (50,150), font, 2, (0,0,255), 3)
            # Overlaying text based on blinking and gaze ratios
            if gaze_ratio <= 0.51:
                cv2.putText(frame, "FANS ON/OFF", (50, 150), font, 2, (0, 0, 255), 3)
                i = 1
                new_frame[:] = (0, 0, 255)
            elif (0.51 < gaze_ratio < 1.5):
                cv2.putText(frame, "no command", (50, 150), font, 2, (0, 0, 255), 3)
                i = 2
            else:
                cv2.putText(frame, "DOOR Open/close", (50, 150), font, 2, (0, 0, 255), 3)
                i = 3
                new_frame[:] = (255, 0, 0)
        if i in command_texts:
            current_time = time.time()
            if confirmed_command == i:
                if current_time - confirmation_start_time >= confirmation_time:
                    print(command_texts[i])  # Perform the command
                    if i == 0:
                        toggle_led(led_pin_3)
                    elif i == 1:
                        toggle_led(led_pin_1)
                    elif i == 3:
                        toggle_led(led_pin_2)
                    confirmed_command = None  # Reset confirmed command
            else:
                confirmation_start_time = current_time
                confirmed_command = i
    cv2.imshow("Frame", frame)  # Displaying the original frame with overlays
    cv2.imshow("New Frame", new_frame)  # Displaying the additional visualizations

    key = cv2.waitKey(1)  # Waiting for a key press to exit
    if key == 27:
        break
GPIO.cleanup()
picam2.stop()  # Releasing the video capture object
cv2.destroyAllWindows()  # Closing all OpenCV windows