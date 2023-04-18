import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import Computervision as computerVision

kit = ServoKit(channels=16) # initialize the servo kit, this has to be put on top of all the classes to make sure it gets set up properly

#PIN TABLE
# 21 = LEDS
# 20 = BUTTON
# 19 = SWITCH 

class Lights:

    def __init__(self):
        GPIO.setwarnings(False) 
        GPIO.cleanup # make sure there is no residue left from past GPIO usage
        GPIO.setmode(GPIO.BCM) # use the BCM type of naming for the pins
        GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW) # put the pin that is connected to the leds on output

    def doLights(self):
        GPIO.output(21, GPIO.HIGH)  # Turn on leds
        time.sleep(0.5) # breathing room

    def dontLights(self):
        GPIO.output(21, GPIO.LOW)  # Turn off leds
        time.sleep(0.5) # breathing room

class DiceTower:

    def rollDice(self, amountOfFloors, waitBetweenFloors): 
        # when this method is called you can tell the system how many floors there are availible 
        # and how long you want the system to keep the floors open for
        for x in range(0,int(amountOfFloors)): # first the for loop that handles the floors
            print("vloer", x + 1, ' is nu instabiel') # print so you know what is happening inside of the tower
            kit.servo[x].angle = 180 # open the current floor
            time.sleep(waitBetweenFloors) # wait said amount of time
            kit.servo[x].angle = 0 # close the current floor
            time.sleep(0.5) # give some time to close the floor before moving on to the next one
        print("de steen heeft de toren verlaten, ik herhaal, de steen heeft de toren verlaten!") # feedback

class Input:

    isCamOn = False 

    def __init__(self):
        GPIO.setmode(GPIO.BCM) # use the BCM type of naming for the pins
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # put the pin that is connected to the button on input
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # put the pin that is connected to the switch on input

    def checkButton(self):
        if GPIO.input(20) == GPIO.HIGH: # check if button is pressed
            while GPIO.input(20) == GPIO.HIGH: # wait for the button to be released to make sure it is on the rising edge
                time.sleep(1)                  # this also helps fight a bit of the debouncing
            print("PAS OP DE DICE WORD GEGOOID!") # print to know what is happening inside of the tower
            diceTower.rollDice(6, 0.5) # calling the method that opens and closes the floors
                
    def checkSwitch(self):
        if GPIO.input(19) == GPIO.HIGH: # check if the button is pressed
            if input.isCamOn == False: # this if statement makes sure that the next few lines only get triggered ONLY once
                input.isCamOn = True
                print("Camera zegt hallo!") # print for feedback
                lights.doLights() # turn on the lights
                
        else: # if the button is not pressed
            if input.isCamOn == True: # this if statement makes sure that the next few lines only get triggered ONLY once
                input.isCamOn = False
                print("Camera zegt doei!") # print for feedback
                lights.dontLights() # turn on the lights
                computerVision.cam.destroy_window() # make sure the windows of the cam actually get closed.
                
diceTower = DiceTower()
input = Input()
lights = Lights()