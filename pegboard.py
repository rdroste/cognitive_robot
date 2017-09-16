import numpy as np
import cv2

# Detect and store the coordinates of all the black rectangles
#   Input: initImg, grayscale image
#   Output: List of rectangle coordinates of the pegboard hole positions
def initPegboard(initImg):

    kernel = np.ones((5, 5), np.float32) / 25
    initImg = cv2.filter2D(initImg, -1, kernel)

    myList = []

    ret, thresh = cv2.threshold(dst, 145, 255, 0)
    _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(6):
        x, y, w, h = cv2.boundingRect(contours0[i])
        myList.append((x, y, w, h))
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return myList

# Check if a rectangle is occupied by a peg
#   Input: initImg, initial image of the board
#   Input: rect, list containing x,y,w,h of the rectangle to consider
#   Input: currImg, current image to check for
#   Output: List of rectangle coordinates of the pegboard hole positions
def checkRectOccupancy(initImg, rect, currImg):

    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    diffMat = initImg[y:y+h, x:x+w] - currImg[y:y+h, x:x+w]

    return cv2.sumElems(diffMat*diffMat)

if __name__ == '__main__':

    cap = cv2.VideoCapture("peg.avi")
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('contours', img)

    cv2.waitKey()
    cv2.destroyAllWindows()

    # rectPosList = initPegboard(img.copy())

    # ret, thresh = cv2.threshold(dst, 145, 255, 0)
    # h, w = img.shape[:2]

    # _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

    # cv2.drawContours(frame, contours0, -1, (0, 255, 0), 2)

    # cv2.imshow('contours', frame)

    # cv2.waitKey()
    # cv2.destroyAllWindows()
