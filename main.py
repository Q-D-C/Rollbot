import MECHCLASSES as mech
import Computervision as cam

while True: #mainloo
    mech.input.checkButton() # when button is pressed dice will be rolled
    mech.input.checkSwitch() # when switch is on camera will be on
    cam.cam.show_frame()     # the main loop that actually shows the camera

# just for testing purposes
# mech.diceTower.rollDice(6, 0.5)
