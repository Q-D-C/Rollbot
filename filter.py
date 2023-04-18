import cv2
import numpy as np
import Computervision as vis
import MECHCLASSES as mech


# class Filter:

#     # def convertcolor(self):
#     #     gray = cv2.cvtColor(vis.Camera.get_frame(self), cv2.COLOR_RGB2GRAY)
#     #     return gray

#     def convertcolor(self, frame):
#         gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#         return gray


#     def blur(self, frame):
#         gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#         blurred = cv2.blur(gray, (3, 3))
#         return blurred

#     def threshold(self, blurred):
#         ret, th1 = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
#         return th1

#     def contours(self, th1):
#         contour, _ = cv2.findContours(
#             th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         return contour

#     def drawcontours(self, contour, frame):
#         draw = cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
#         return draw

#     def printcontour(self, contour, draw):
#         nummer = len(contour)

#         if nummer < 7 and nummer > 0 and mech.input.isCamOn == True:
#                cv2.putText(draw, str(nummer), (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         return nummer
            
# filter = Filter()


class Filter:

    def convertcolor(self):
        gray = cv2.cvtColor(vis.Camera.get_frame(self), cv2.COLOR_BGR2GRAY)
        return gray


    def blur(self, gray):
        blurred = cv2.blur(gray, (3, 3))
        return blurred

    def threshold(self, blurred):
        ret, th1 = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
        return th1

    def contours(self, th1):
        contour, _ = cv2.findContours(
            th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contour

    def drawcontours(self, contour):
        draw = cv2.drawContours(vis.Camera.get_frame(self), contour, -1, (0, 255, 0), 3)
        return draw

    def printcontour(self, contour, draw):
        nummer = len(contour)

        if nummer < 24 and nummer > 0:
               cv2.putText(draw, str(nummer), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return nummer
            
filter = Filter()