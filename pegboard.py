import numpy as np
import cv2

# Detect and store the coordinates of all the black rectangles
#   Input: initImg, grayscale image
#   Output: List of rectangle coordinates of the pegboard hole positions
def initPegboard(initImg):

    kernel = np.ones((5, 5), np.float32) / 25
    initImg = cv2.filter2D(initImg, -1, kernel)

    myList = []

    # Everything higher than the threshold is set to white
    threshold = 100
    ret, thresh = cv2.threshold(initImg, threshold, 255, 0)
    _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Min and Max area for the rectangles
    minArea = 1000.0
    maxArea = 15000.0

    for i in range(len(contours0)): #range(6):
        area = cv2.contourArea(contours0[i])
        if (area > minArea) & (area < maxArea):
            cv2.drawContours(initImg, contours0, i, color=255, thickness=-1)

            # Access the image pixels and create a 1D numpy array then add to list
            pts = np.where(initImg == 255)
            myList.append(pts)

            # x, y, w, h = cv2.boundingRect(contours0[i])
            # myList.append((x, y, w, h))
            #cv2.rectangle(initImg, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return myList

# Check if a rectangle is occupied by a peg
#   Input: initImg, initial image of the board
#   Input: rect, list containing pixels of the rectangle to consider
#   Input: currImg, current image to check for
#   Output: List of rectangle coordinates of the pegboard hole positions
def checkRectOccupancy(initImg, currImg, rect):

    diffMat = initImg[rect] - currImg[rect]
    return cv2.sumElems(diffMat*diffMat)[0]

# Asses the routine
def assessRoutine(initImg, currImg, rectList):

    score = checkRectOccupancy(initImg, currImg, rectList[2])
    return score
