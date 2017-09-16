
import numpy as np
import cv2

def run(nCoins, roi_coords):

    results = {'no_successful_coins': 0, 'times': np.zeros(nCoins), 'traj_scores': np.zeros(nCoins)}

    cap = cv2.VideoCapture("./coin_test_1.mp4")
    # while not cap.isOpened():
    #     cap = cv2.VideoCapture("./out.mp4")
    #     cv2.waitKey(1000)
    #     print "Wait for the header"

    # roi_size = roi_coords[:,1] - roi_coords[:,0]
    # roi = np.zeros((roi_size[0], roi_size[1]))

    while True:
        ret, frame = cap.read()

        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            roi = img[roi_coords[0,0]:roi_coords[0,1], roi_coords[1,0]:roi_coords[1,1]]
            roi = cv2.GaussianBlur(roi, (21, 21), 0)

            cv2.imshow('image', roi)
            cv2.waitKey(1)

        else:
            break

    cap.release()


    return results