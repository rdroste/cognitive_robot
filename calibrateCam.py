import numpy as np
import cv2
import utils
import time

# Main routine
#if __name__ == '__main__':

# Check Pegboard
cv2.destroyAllWindows()

cap = utils.prepare_camera(3)
time.sleep(2)
ret, frame = cap.read()
time.sleep(2)
frame = frame[370:460, 240:400]
cv2.imshow('image', frame)
cv2.waitKey()
#
# # Check Coin
# ret, frame = cap.read()
# roi_coords = np.array([[282, 349], [219, 282]])
# frame = frame[roi_coords[0, 0]:roi_coords[0, 1], roi_coords[1, 0]:roi_coords[1, 1]]
# cv2.imshow('image', frame)
# cv2.waitKey()
#
utils.close_camera(cap)