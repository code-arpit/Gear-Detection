import cv2 as cv 
import numpy as np

def count_teeth(image, teeths):
    
    raw_image = cv.imread(image)

    # blank_image = np.copy(raw_image)
    # cv.imshow('gray image', gray_image)

    bilateral_filter_image = cv.bilateralFilter(raw_image, 5, 175, 175)
    # cv.imshow('bilateral filtered image', bilateral_filter_image)

    blurred_image = cv.medianBlur(bilateral_filter_image, 5)

    edges_image = cv.Canny(blurred_image, 100, 200)
    # cv.imshow('edges image', edges_image)

    ret, contours = cv.findContours(edges_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours_list = []

    for c in ret:
        perimeter =cv.arcLength(c, True)
        approx =cv.approxPolyDP(c, 0.01*perimeter, True)
        area = cv.contourArea(c)
        if((len(approx) > 5) & (len(approx) < 25) & (area > 50)):
            contours_list.append(c)

    cv.drawContours(raw_image, contours_list, -1, (0,0,255), 2)
    # cv.imshow('contours', blank_image)
    contour_length = f"number of contours detected : {len(ret)}"
    # print(contour_length)

    contour = max(ret, key = cv.contourArea)
    #centroid of gear
    M = cv.moments(contour)
    contour_X = int (M["m10"] / M["m00"])
    contour_Y = int(M["m01"] / M["m00"])

    center = cv.circle(raw_image, (contour_X,contour_Y), 3, (0,0,255), -1)
    # cv.imshow('contours', raw_image)

    #curve of contour
    curve = cv.convexHull(contour, clockwise=True, returnPoints= False)
    cv.drawContours(raw_image, contour[curve], -1, (0,0,255), 2)

    #combibining near by curve points
    curve_near = []
    for i in curve:
        if (len(curve_near) == 0):
            curve_near.append(i)
        else:
            difference = contour[i] - contour[curve_near[-1]]
            if (cv.norm(difference)>19):
                curve_near.append(i)

    curve_near = np.asarray(curve_near)
    cv.drawContours(raw_image, contour[curve_near], -1, (255,0,0), 5)

    # cv.imshow('points on curve', raw_image)
    teeths = len(contour[curve_near])
    cv.putText(raw_image,f'{teeths}',(20,20), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))
    print(f'Number of teeths found = {teeths}')
    # cv.waitKey(0)
    image = raw_image
    return (teeths)

image = 'gear.jpg'
teeths =0
count_teeth(image, teeths)