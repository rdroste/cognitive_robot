import numpy as np
import cv2
import os
import pegboard as peg
import vision_coin, utils

DEBUG = True

nCoins = 3
# emotion_key = os.environ['MICROSOFT_EMOTION']

# Main routine
if __name__ == '__main__':

    # Initialize all the connections with yumi and the camera
    if DEBUG:
        cap = cv2.VideoCapture("peg_test.avi")
    else:
        cap = utils.prepare_camera()

    # Yumi says hi and explains the experiment

    # Test 1: The pegboard experiment

    # Yumi explains the pegboard experiment

    # Start the experiment
    # Initialize the pegboard
    ret, frame = cap.read()
    if ret:

        initImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 480, 640
        initImg = initImg[250:350, 230:470]
        cv2.imshow('image', initImg)
        cv2.waitKey()

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
        frame = frame[250:350, 230:470]
        currImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        score = peg.assessRoutine(initImg, currImg, rectList)


    roi_coords = np.array([[323, 472], [243, 411]]) # [[411, 243], [472, 323]] for coin_test_1.mp4
    # results = vision_coin.run(3, roi_coords)
    if DEBUG:
        cap = cv2.VideoCapture("./coin_test_1.mp4")

    # Yumi explains the coin experiment

    # Start the experiment

    # Initialize test 2: The coin experiment
    roi_coords = np.array([[323, 472], [243, 411]])  # [[411, 243], [472, 323]] for coin_test_1.mp4
    ref_n_frames = 3
    sos_n_frames = 16
    asos_train = 5
    asos_thr_factor = 20
    coin_thr = 60

    roi_size = roi_coords[:, 1] - roi_coords[:, 0]
    asos_array = np.zeros(asos_train)
    reference = np.zeros(roi_size)
    ref_frames = np.zeros((roi_size[0], roi_size[1], ref_n_frames))
    sos_array = np.zeros(sos_n_frames)

    roi_counter = 0
    frame_counter = 0
    asos_train_counter = 0
    coin_frame = -1000
    asos_thr = 0
    coin_counter = 0

    # Throw away the first frames
    for i in range(20):
        cap.read()

    expRunning = True
    while expRunning:

        ret, frame = cap.read()
        if not ret:
            expRunning = False
            continue

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Motion Tracking here...
        # if frame_counter > 20 and frame_counter % 60:
        #     utils.save_image(img, './tmp.png')
        #     utils.get_emotion('./tmp.png', emotion_key)

        # Detect coin in ROI
        if frame_counter % 2 == 0:
            # Get roi and blur
            roi = img[roi_coords[0,0]:roi_coords[0,1], roi_coords[1,0]:roi_coords[1,1]]
            roi = cv2.GaussianBlur(roi, (21, 21), 0)

            # Get frame for reference and update reference if necessary
            ref_frames[:,:, roi_counter % ref_n_frames] = roi
            if roi_counter % ref_n_frames == ref_n_frames - 1:
                reference = np.mean(ref_frames, axis=2)

            # If a reference has been created and the last coin is some frames ago, compute SOS
            if roi_counter >= ref_n_frames - 1 and frame_counter - coin_frame > coin_thr:
                sos_array[roi_counter % sos_n_frames] = np.sum(np.square(roi - reference))

                # If the SOS array is full, compute the average
                if roi_counter % sos_n_frames == sos_n_frames - 1:
                    asos = np.mean(sos_array)

                    # Compute a few average SOS to set the threshold
                    if asos_train_counter < asos_train:
                        asos_array[asos_train_counter] = asos
                        if asos_train_counter == asos_train - 1:
                            asos_thr = asos_thr_factor * np.mean(asos_array)
                        asos_train_counter = asos_train_counter + 1

                    # Check if asos threshold is exceeded
                    else:
                        if asos > asos_thr:
                            coin_counter = coin_counter + 1
                            print (coin_counter)
                            if coin_counter == nCoins:
                                expRunning = False
                            sos_array = np.zeros(sos_n_frames)
                            coin_frame = frame_counter

            if DEBUG:
                cv2.imshow('image', roi)
                cv2.waitKey(1)
                roi_counter = roi_counter + 1

        # Feed the image to sentiment analysis

        frame_counter = frame_counter + 1

    utils.close_camera(cap)