import numpy as np
import cv2

# Main routine
if __name__ == '__main__':

    # Check Pegboard
    cap = utils.prepare_camera()
    ret, frame = cap.read()
    frame = frame[250:350, 230:470]
    cv2.imshow('image', frame)
    cv2.waitKey()

    # Check Coin
    ret, frame = cap.read()
    roi_coords = np.array([[282, 349], [219, 282]])
    frame = frame[roi_coords[0, 0]:roi_coords[0, 1], roi_coords[1, 0]:roi_coords[1, 1]]
    cv2.imshow('image', frame)
    cv2.waitKey()

    utils.close_camera(cap)