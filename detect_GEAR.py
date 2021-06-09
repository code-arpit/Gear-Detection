from tkinter import *
import cv2 as cv 
import numpy as np
from Config import *

class detect_teeth:
    def __init__(self, image, teeths=0):
        image = cv.imread(image)
        self.raw_image = image
        self.teeths = teeths
        
    def teeth(self):    
        self.bilateral_filter_image = cv.bilateralFilter(self.raw_image, 5, getBilateralFilter_sigmaColor(), getBilateralFilter_sigmaSpace())
        # cv.imshow('bilateral filtered image', self.bilateral_filter_image)
        self.blurred_image = cv.medianBlur(self.bilateral_filter_image, getMedian_Blurr())

        self.edges_image = cv.Canny(self.blurred_image, getCanny_thresh1(), getCanny_thresh2())
        # cv.imshow('edges image', self.edges_image)
        ret, contours = cv.findContours(self.edges_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        self.contours_list = []

        for c in ret:
            perimeter =cv.arcLength(c, True)
            approx =cv.approxPolyDP(c, 0.01*perimeter, True)
            area = cv.contourArea(c)
            if((len(approx) > 5) & (len(approx) < 25) & (area > 50)):
                self.contours_list.append(c)

        cv.drawContours(self.raw_image, self.contours_list, -1, (0,0,255), 2)
        # cv.imshow('contours', self.raw_image)
        self.contour_length = f"number of contours detected : {len(ret)}"
        # print(self.contour_length)

        self.contour = max(ret, key = cv.contourArea)
        # #centroid of gear
        M = cv.moments(self.contour)
        contour_X = int (M["m10"] / M["m00"])
        contour_Y = int(M["m01"] / M["m00"])

        cv.circle(self.raw_image, (contour_X,contour_Y), 3, (0,0,255), -1)
        # cv.imshow('contours', self.raw_image)

        # #curve of contour
        curve = cv.convexHull(self.contour, clockwise=True, returnPoints= False)
        # cv.drawContours(self.raw_image, self.contour[curve], -1, (0,0,0), 4)
        # cv.imshow('contours', self.raw_image)
        
        #combibining near by curve points
        self.curve_near = []
        for i in curve:
            if (len(self.curve_near) == 0):
                self.curve_near.append(i)
            else:
                last = self.curve_near[-1]
                difference = self.contour[i] - self.contour[last]
                if (cv.norm(difference) > getMin_Near_Curve()):
                    self.curve_near.append(i)

        self.curve_near = np.asarray(self.curve_near)
        self.raw_image = cv.drawContours(self.raw_image, self.contour[self.curve_near], -1, (255,0,0), 5)
        # cv.imshow('points on curve', self.raw_image)
        # print(self.raw_image)
        self.teeths = len(self.contour[self.curve_near])
        
        # cv.putText(self.raw_image,f'{self.teeths}',(20,20), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))
        
        # print(f'Number of teeths found = {self.teeths}')
        return (self.raw_image, self.teeths)

# image = 'gear.jpg'
# c = detect_teeth(image, teeths=0)

# cv.imshow('show teeth', c.teeth()[0])
# print(c.teeth()[1])
# cv.waitKey(0)