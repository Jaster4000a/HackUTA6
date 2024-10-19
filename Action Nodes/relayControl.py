import RPi.GPIO as GPIO
import time

class relayController():
    def __init__(self,pin=15):
        self.pin=pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)

    def relayOn(self):
        GPIO.output(self.pin,1)

    def relayOff(self):
        GPIO.output(self.pin,0)

    def dripTime(self,seconds):
        self.relayOn()
        time.sleep(seconds)
        self.relayOff()

if __name__ == "__main__":
    relayClient = relayController()

    relayClient.relayOn()
    time.sleep(1)
    relayClient.relayOff()
    time.sleep(1)
