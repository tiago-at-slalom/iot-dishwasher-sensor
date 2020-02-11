import RPi.GPIO as GPIO 

class PowerSensor:
    sensor = None
    INPUT_PIN = -1 # Raspberry Pi pin number to read the sensor values

    def __init__(self, input_pin):
        self.INPUT_PIN = input_pin
        try:
            GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
            GPIO.setup(self.INPUT_PIN, GPIO.IN)           # Set our input pin to be an input
        except:
            print("Exception: Problem connecting to Input")
    
    def isMachineWorking(self):
        try:
            result = GPIO.input(self.INPUT_PIN)
            return result == True
        except Exception as ex:
            print("Exception: Problem reading sensor values")
            print(ex)
            return False
