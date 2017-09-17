import numpy as np
import cv2
import utils


# # Check Pegboard
cap = utils.prepare_camera(3)
# ret, frame = cap.read()
# frame = frame[370:460, 240:400]
# cv2.imshow('image', frame)
# cv2.waitKey()

# Check Coin
ret, frame = cap.read()
roi_coords = np.array([[350, 430], [130, 230]])
frame = frame[roi_coords[0, 0]:roi_coords[0, 1], roi_coords[1, 0]:roi_coords[1, 1]]
cv2.imshow('image', frame)
cv2.waitKey()

utils.close_camera(cap)
