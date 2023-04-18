import cv2
from cv2 import WINDOW_NORMAL
import numpy as np
import filter as fil
import MECHCLASSES as mech

video_capture = cv2.VideoCapture('/dev/video0')

class Camera():

    def __init__(self):
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
        print('Camera staat klaar!!! naja hangt klaar...')

    def get_frame(self):

        ret, frame = video_capture.read()

        return frame

    def destroy_window(self):
        cv2.destroyAllWindows()

    def show_frame(self):
        
        if mech.input.isCamOn == True:
            gray = fil.filter.convertcolor()
            th1 = fil.filter.threshold(fil.filter.blur(gray))
            drawing = fil.filter.drawcontours(fil.filter.contours(th1))
            nummer = fil.filter.printcontour(fil.filter.contours(th1), drawing)

            if nummer < 24 and nummer > 0:
                cv2.putText(drawing, str(nummer), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.namedWindow('RollBot',WINDOW_NORMAL)
            cv2.resizeWindow('RollBot',500,400)
            cv2.imshow('RollBot', drawing)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.destroy_window()

            return False
        return True

cam = Camera()