import numpy as np
import cv2
import math

# Detect and store the coordinates of all the black rectangles
#   Input: initImg, grayscale image
#   Output: List of rectangle coordinates of the pegboard hole positions
def initPegboard(initImg):

    kernel = np.ones((5, 5), np.float32) / 25
    initImg = cv2.filter2D(initImg, -1, kernel)

    myList = []

    # Everything higher than the threshold is set to white
    threshold = 150

    ret, thresh = cv2.threshold(initImg, threshold, 255, 0)
    _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Min and Max area for the rectangles
    minArea = 200.0
    maxArea = 500.0

    for i in range(len(contours0)): #range(6):
        area = cv2.contourArea(contours0[i])
        tempMat = initImg.copy()
        if (area > minArea) & (area < maxArea):
            cv2.drawContours(tempMat, contours0, i, color=255, thickness=-1)

            # Access the image pixels and create a 1D numpy array then add to list
            pts = np.where(tempMat == 255)
            tempMat = initImg.copy()

            myList.append(pts)

    return myList

# Check if a rectangle is occupied by a peg
#   Input: initImg, initial image of the board
#   Input: rect, list containing pixels of the rectangle to consider
#   Input: currImg, current image to check for
#   Output: List of rectangle coordinates of the pegboard hole positions
def checkRectOccupancy(initImg, currImg, rect):

    diffMat = initImg[rect].astype(np.double) - currImg[rect].astype(np.double)
    optMat = 255*np.ones((len(diffMat))) - initImg[rect].astype(np.double)
    optScore = np.sum(np.square(optMat))/len(diffMat)
    currScore = np.sum(np.square(diffMat))/len(diffMat)
    if currScore/optScore > 0.3:
        return 0.5*(currScore+optScore)/optScore
    else:
        return 0.0

# Asses the routine
def assessRoutine(initImg, currImg, rectList):
    score = []
    for i in range(6):
        currScore = checkRectOccupancy(initImg, currImg, rectList[i])

        score.append(currScore)
    print score
    return score
