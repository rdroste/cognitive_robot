import numpy as np
import cv2

if __name__ == '__main__':

    cap = cv2.VideoCapture("vid.avi")
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    h, w = img.shape[:2]

    _, contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

    cv2.drawContours(frame, contours0, -1, (0, 255, 0), 2)

    cv2.imshow('contours', frame)

    cv2.waitKey()
    cv2.destroyAllWindows()