import cv2      # OpenCV for computer vision tasks
import numpy as np   # NumPy for numerical operations
import dlib  # dlib for face detection and facial landmark detection
from math import hypot   # Importing hypot function from math module
import time  # Import the time module for timer functionality
import voiceDetection as voice
import hands2 as hd
import sys


def adjust_brightness(frame, brightness_factor):
    # Convert frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply brightness adjustment to the Value channel
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_factor, 0, 255)

    # Convert the frame back to BGR color space
    brightened_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return brightened_frame

def main():
    # Initializing video capture from default camera (index 0)
    cap = cv2.VideoCapture(0)
    # Inside your main loop
    brightness_factor = 0.75  # Adjust this value to change brightness, 0.5 for half brightness
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



        cv2.polylines(mask, [left_eye_region], True, 255, 2)


        cv2.fillPoly(mask, [left_eye_region], 255)

        # Applying the mask to extract the left eye
        eye = cv2.bitwise_and(gray, gray, mask=mask)

        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])


        gray_eye = eye[min_y:max_y, min_x:max_x]


        _, threshold_eye = cv2.threshold(gray_eye, 40, 255, cv2.THRESH_BINARY)


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

        0: "Blink Detected",
        1: "Left",
        2: "no command",
        3: "right"
    }

    # Initialize confirmation variables
    confirmation_time = 5  # Confirmation time in seconds
    confirmation_start_time = 0
    confirmed_command = None
    i = -1

    while (True):
        _, frame = cap.read() # Reading a frame from the video capture
        frame = cv2.resize(frame,None, fx=0.5,fy=0.5)
        # Apply brightness adjustment
        frame = adjust_brightness(frame, brightness_factor)
        new_frame = np.zeros((500, 500, 3), np.uint8)   # Creating a blank frame for additional visualizations
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converting the frame to grayscale

        faces = detector(gray)  # Detecting faces in the grayscale frame
        for face in faces:

            #         face detection
            #         x,y = face.left(),face.top()
            #         x1,y1 = face.right(),face.bottom()
            #         cv2.rectangle(frame, (x,y),(x1,y1),(0,255,0),2)
            # Calculating blinking ratio for both eyes
            landmarks = predictor(gray, face)   # Predicting facial landmarks for the detected face


            # Detecting gaze direction

            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)

            # Calculating the average blinking ratio by summing the ratios of the left and right eyes and dividing by 2
            # The blinking ratio indicates the extent of eyelid closure, with higher values indicating more closed eyelids

            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

            # Overlaying text based on blinking and gaze ratios

            #print(blinking_ratio)
            #print("blink ratio:")
            if (blinking_ratio > 4.5):
                cv2.putText(frame, "Blink", (50, 100), font, 1, (0, 0, 255), 2)
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
                print(gaze_ratio)
                if gaze_ratio <= 0.83:
                    cv2.putText(frame, "Left", (50, 100), font, 1, (0, 0, 255), 2)
                    i = 1
                    new_frame[:] = (0, 0, 255)
                elif (0.83< gaze_ratio <0.94) :
                    cv2.putText(frame, "center", (50, 100), font, 1, (0, 0, 255), 2)
                    i = 2
                else:
                    cv2.putText(frame, "Right", (50, 100), font, 1, (0, 0, 255), 2)
                    i = 3
                    new_frame[:] = (255, 0, 0)
            if i in command_texts:
                    current_time = time.time()
                    if confirmed_command == i:
                        if current_time - confirmation_start_time >= confirmation_time:
                            print(command_texts[i])  # Perform the command
                            confirmed_command = None  # Reset confirmed command
                    else:
                        confirmation_start_time = current_time
                        confirmed_command = i

            cv2.imshow("Frame", frame)  # Displaying the original frame with overlays
            cv2.imshow("New Frame", new_frame)  # Displaying the additional visualizations

        # Exit the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('x'):
            sys.exit()
        if cv2.waitKey(1) & 0xFF == ord('h'):
            cap.release()
            cv2.destroyAllWindows()
            hd.main()
        if cv2.waitKey(1) & 0xFF == ord('v'):
            cap.release()
            cv2.destroyAllWindows()
            voice.main()


    cap.release()   # Releasing the video capture object
    cv2.destroyAllWindows()     # Closing all OpenCV windows
