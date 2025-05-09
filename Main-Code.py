import cv2
import os
import time
import voiceDetection as voice
import hands2 as hd
import eyes2 as eyes
from simple_facerec import SimpleFacerec
import sys

user_input = 'a'
# Function to capture an image and save it in a directory with the provided name
def capture_image(name):
    # Create a directory with the user's name if it doesn't exist already
    directory = f"images/{name.lower()}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Capture an image and save it inside the created directory
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    filename = f"{directory}/{name.lower()}.jpeg"
    cv2.imwrite(filename, frame)
    cap.release()
    cv2.destroyAllWindows()

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

while True:
    print("Choose an option:")
    print("1. Log in")
    print("2. Create account")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # Log in
        user_input = 'a'
        duration = 5 # 5 seconds
        hassan_detected = False

        current_user = input("Enter your name: ").lower()
        # Initialize timer variables
        timer_start = time.time()
        # Encode faces from a folder
        sfr = SimpleFacerec()
        sfr.load_encoding_images(f"images/{current_user}")


        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            # Detect Faces
            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
                if name == current_user and not hassan_detected:
                    hassan_detected = True
                    # Initialize timer variables
                    timer_start = time.time()

            # Check if the specified duration has passed and the user is still detected
            if time.time() - timer_start >= duration and hassan_detected:
                user_input = input("Enter character: ('E' or 'V' or 'H') ")
                break
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        while True:
            # Perform actions based on user input
            if user_input.lower() == 'e':
                eyes.main()
            elif user_input.lower() == 'v':
                cap.release()  # Releasing the video capture object
                cv2.destroyAllWindows()  # Closing all OpenCV windows
                voice.main()
            elif user_input.lower() == 'h':
                hd.main()
            else:
                cap.release()  # Releasing the video capture object
                cv2.destroyAllWindows()  # Closing all OpenCV windows
                break

            user_input = input("Enter a character to choose another feature ('E' or 'V' or 'H') or 'X' to exit")

    elif choice == '2':
        # Create account
        name = input("Enter your name: ")
        capture_image(name)
        verification_input = input("Enter the verification code that was sent to you by sms")
        if verification_input == 123:   # let us assume that the code that was sent was 123
            break
        print(f"Account created successfully for {name}.")


    else:
        print("Invalid choice. Please enter '1' or '2'.")
    if user_input.upper() == 'X':
        break
    continue_choice = input("Do you want to continue? (yes/no): ")
    if continue_choice.lower() != 'yes':
        break
