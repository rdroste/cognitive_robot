from __future__ import print_function

import numpy as np
import cv2

def run(nCoins, roi_coords):

    results = {'n_successful_coins': 0, 'times': np.zeros(nCoins), 'traj_scores': np.zeros(nCoins)}

    cap = cv2.VideoCapture("./coin_test_1.mp4")

    roi_size = roi_coords[:,1] - roi_coords[:,0]

    ref_n_frames = 3
    sos_n_frames = 16
    ssos_train = 5
    ssos_thr_factor = 20
    coin_thr = 60

    ssos_array = np.zeros(ssos_train)
    reference = np.zeros(roi_size)
    ref_frames = np.zeros((roi_size[0], roi_size[1], ref_n_frames))
    sos_array = np.zeros(sos_n_frames)

    roi_counter = 0
    frame_counter = 0
    ssos_train_counter = 0
    coin_frame = -1000
    ssos_thr = 0
    coin_counter = 0

    for i in range(20):
        cap.read()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Motion Tracking here...

        # Detect coin in ROI
        if frame_counter % 2 == 0:
            roi = img[roi_coords[0,0]:roi_coords[0,1], roi_coords[1,0]:roi_coords[1,1]]
            roi = cv2.GaussianBlur(roi, (21, 21), 0)

            ref_frames[:,:, roi_counter % ref_n_frames] = roi
            if roi_counter % ref_n_frames == ref_n_frames - 1:
                reference = np.mean(ref_frames, axis=2)

            if roi_counter >= ref_n_frames - 1 and frame_counter - coin_frame > coin_thr:
                sos_array[roi_counter % sos_n_frames] = np.sum(np.square(roi - reference))

                if roi_counter % sos_n_frames == sos_n_frames - 1:
                    ssos = np.sum(sos_array)
                    if ssos_train_counter < ssos_train:
                        ssos_array[ssos_train_counter] = ssos
                        if ssos_train_counter == ssos_train - 1:
                            ssos_thr = ssos_thr_factor * np.mean(ssos_array)
                        ssos_train_counter = ssos_train_counter + 1
                    else:
                        if ssos > ssos_thr:
                            coin_counter = coin_counter + 1
                            print (coin_counter)
                            if coin_counter == nCoins:
                                break
                            sos_array = np.zeros(sos_n_frames)
                            coin_frame = frame_counter

            cv2.imshow('image', roi)
            cv2.waitKey(1)
            roi_counter = roi_counter + 1

        frame_counter = frame_counter + 1

    cap.release()

    results['n_successful_coins'] = coin_counter

    return results