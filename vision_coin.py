from __future__ import print_function

import numpy as np
import cv2

def run(nCoins, roi_coords):

    results = {'no_successful_coins': 0, 'times': np.zeros(nCoins), 'traj_scores': np.zeros(nCoins)}

    cap = cv2.VideoCapture("./coin_test_1.mp4")

    roi_size = roi_coords[:,1] - roi_coords[:,0]

    ref_n_frames = 5
    sos_n_frames = 30
    ssos_train = 5
    ssos_thr_factor = 20

    ssos_array = np.zeros(ssos_train)
    reference = np.zeros(roi_size)
    ref_frames = np.zeros((roi_size[0], roi_size[1], ref_n_frames))
    sos_array = np.zeros(sos_n_frames)

    movement = False
    frame_counter = 0
    ssos_train_counter = 0

    for i in range(20):
        cap.read()

    while True:
        ret, frame = cap.read()

        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            roi = img[roi_coords[0,0]:roi_coords[0,1], roi_coords[1,0]:roi_coords[1,1]]
            roi = cv2.GaussianBlur(roi, (21, 21), 0)

            ref_frames[:,:, frame_counter % ref_n_frames] = roi
            if frame_counter % ref_n_frames == ref_n_frames - 1:
                reference = np.mean(ref_frames, axis=2)

            if frame_counter >= ref_n_frames - 1:
                sos_array[frame_counter % sos_n_frames] = np.sum(np.square(roi - reference))

            if frame_counter % sos_n_frames == sos_n_frames - 1:
                ssos = np.sum(sos_array)
                if ssos_train_counter < ssos_train:
                    ssos_array[ssos_train_counter] = ssos
                    if ssos_train_counter == ssos_train - 1:
                        ssos_thr = ssos_thr_factor * np.mean(ssos_array)
                    ssos_train_counter = ssos_train_counter + 1
                else:
                    if ssos > ssos_thr:
                        movement = True
                        print('MOVEMENT')
                    else:
                        movement = False

            cv2.imshow('image', roi)
            cv2.waitKey(1)

            frame_counter = frame_counter + 1
        else:
            break

    cap.release()


    return results