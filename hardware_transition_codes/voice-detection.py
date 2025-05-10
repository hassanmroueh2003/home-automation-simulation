import speech_recognition as sr
import RPi.GPIO as GPIO
import time

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

# Function to turn LED on
def turn_on_led(pin):
    GPIO.output(pin, GPIO.HIGH)

# Function to turn LED off
def turn_off_led(pin):
    GPIO.output(pin, GPIO.LOW)

# Function to record audio and convert speech to text
def speech_to_text():
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)  # Listen to the audio

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)  # Recognize speech using Google Speech Recognition
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))
        return ""

# Initialize recognizer
recognizer = sr.Recognizer()

try:
    while True:
        # Call the function to start speech-to-text conversion
        result = speech_to_text()
        if result == "exit":
            print("Exiting the program...")
            break

        # Check for voice commands and control LEDs accordingly
        if "turn off the lights" in result:
            turn_off_led(led_pin_1)
        elif "turn on the lights" in result:
            turn_on_led(led_pin_1)
        elif "turn off the fan" in result:
            turn_off_led(led_pin_2)
        elif "turn on the fan" in result:
            turn_on_led(led_pin_2)
        elif "turn off the extension" in result:
            turn_off_led(led_pin_3)
        elif "turn on the extension" in result:
            turn_on_led(led_pin_3)

        # Wait for 5 seconds before checking again
        time.sleep(5)

except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Cleanup GPIO
    GPIO.cleanup()