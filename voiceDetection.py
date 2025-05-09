import speech_recognition as sr
import hands2 as hd
import eyes2 as eyes
import sys
# Create a recognizer instance
recognizer = sr.Recognizer()

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
        return text  # Return the recognized text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))

def main():
    while True:
        # Call the function to start speech-to-text conversion
        result = speech_to_text()
        if result and result.lower() == "exit":
            print("Exiting the program...")
            sys.exit()
        if result and result.lower() == "eyes":
            eyes.main()
        if result and result.lower() == "hands":
            hd.main()
