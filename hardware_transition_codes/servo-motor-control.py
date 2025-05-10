import RPi.GPIO as GPIO
import time

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the servo motor
SERVO_PIN = 18

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Set the servo pin as an output pin
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM
pwm_frequency = 50  # Set PWM frequency to 50Hz (standard for most servos)
pwm = GPIO.PWM(SERVO_PIN, pwm_frequency)
pwm.start(0)


# Function to rotate the servo clockwise
def rotate_clockwise():
    pwm.ChangeDutyCycle(7.5)  # Adjust duty cycle to rotate clockwise
    time.sleep(1)  # Rotate for 1 second
    pwm.ChangeDutyCycle(0)  # Stop the servo
    time.sleep(1)  # Wait for 1 second


# Function to rotate the servo counterclockwise
def rotate_counterclockwise():
    pwm.ChangeDutyCycle(2.5)  # Adjust duty cycle to rotate counterclockwise
    time.sleep(1)  # Rotate for 1 second
    pwm.ChangeDutyCycle(0)  # Stop the servo
    time.sleep(1)  # Wait for 1 second


try:
    # Rotate clockwise five times
    for _ in range(5):
        rotate_clockwise()

    # Rotate counterclockwise five times
    for _ in range(5):
        rotate_counterclockwise()

except KeyboardInterrupt:
    # If the user presses Ctrl+C, clean up the GPIO configuration
    pwm.stop()
    GPIO.cleanup()
