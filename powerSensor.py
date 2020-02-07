# from gpiozero import SmoothedInputDevice
import RPi.GPIO as GPIO 

class PowerSensor:
    # sensorAdaptor = None # Do we need this?
    sensor = None

    def __init__(self, sa):
        # self.sensorAdaptor = sa
        try:
            # self.sensor = SmoothedInputDevice(14)#, threshold = 1)
            GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
            INPUT_PIN = 14           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
            GPIO.setup(INPUT_PIN, GPIO.IN)           # Set our input pin to be an input
        except:
            print("Exception: Problem connecting to Input")
    
    def isMachineWorking(self):
        try:
            # return self.sensor.is_active()
            return GPIO.input(INPUT_PIN)
        except Exception as ex:
            print("Exception: Problem reading sensor values")
            print(ex)
            return False
