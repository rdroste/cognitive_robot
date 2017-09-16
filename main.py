import numpy as np
import cv2
import pegboard as peg

# Main routine
if __name__ == '__main__':

    # Initialize all the connections with yumi and the camera
    cap = cv2.VideoCapture("peg.avi")

    # Yumi says hi and explains the experiment

    # Test 1: The pegboard experiment

    # Yumi explains the pegboard experiment

    # Start the experiment
    # Initialize the pegboard
    ret, frame = cap.read()
    if ret:
        initImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rectList = peg.initPegboard(initImg.copy())
        expRunning = True
        # Yumi shows the pegboard routine

        # Yumi tells the person to do routine (and countdown maybe?)


        while expRunning:
            # Start facial/behavioral analysis with 10 sec timer
            ret, currImg = cap.read()
            # Feed the image to sentiment analysis

            expRunning = False

        # Evaluate the board
        ret, frame = cap.read()
        currImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        score = peg.assessRoutine(initImg, currImg, rectList)

    # Test 2: The coin experiment
    # Yumi explains the coin experiment

    # Start the experiment

    while expRunning:
        # Start facial/behavioral analysis with 10 sec timer
        ret, frame = cap.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Feed the image to sentiment analysis

        expRunning = false
