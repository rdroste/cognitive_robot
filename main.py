import numpy as np
import cv2
import os, time
import pegboard as peg
import utils
import multiprocessing as mp

DEBUG = True

nCoins = 3
emotion_analysis_skip_frames = 10
filepath = './image.png'
emotion_key = os.environ['MICROSOFT_EMOTION']


def main():

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
    if not ret:
        print("Cannot open camera")
        return -1

    initImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 480, 640
    initImg = initImg[250:350, 230:470]
    cv2.imshow('image', initImg)
    # cv2.waitKey()

    rectList = peg.initPegboard(initImg.copy())
    expRunning = True
    # Yumi shows the pegboard routine

    # Yumi tells the person to do routine (and countdown maybe?)

    # Emotion analysis
    frame_counter = 0
    mp_counter = 0
    r = []
    p = mp.Pool()
    while expRunning:
        ret, frame = cap.read()
        if not ret:
            expRunning = False
            continue
        currImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if frame_counter % emotion_analysis_skip_frames == 0:

            utils.save_image(currImg)
            r.append(p.apply_async(utils.get_emotion, args=(filepath, emotion_key)))
            mp_counter = mp_counter + 1

        frame_counter = frame_counter + 1

        if DEBUG:
            cv2.imshow('image', currImg)
            cv2.waitKey(20)

    emotion_nr_pegs = np.zeros(mp_counter)
    emotion_certainty_pegs = np.zeros(mp_counter)
    for i in range(mp_counter):
        try:
            emotion_nr_pegs[i], emotion_certainty_pegs[i] = r[i].get()
        except:
            emotion_nr_pegs[i], emotion_certainty_pegs[i] = 0, 0
    p.close()
    p.join()
    print(emotion_nr_pegs)
    print(emotion_certainty_pegs)

    # Evaluate the board
    currImg = currImg[250:350, 230:470]
    score = peg.assessRoutine(initImg, currImg, rectList)
    print(score)

    # results = vision_coin.run(3, roi_coords)
    if DEBUG:
        # cap = cv2.VideoCap    ture("./coin_test_1.mp4")
        cap = cv2.VideoCapture("./coin_test_2.avi")

    # Yumi explains the coin experiment

    # Start the experiment

    # Initialize test 2: The coin experiment
    # roi_coords = np.array([[323, 472], [243, 411]])  # [[411, 243], [472, 323]] for coin_test_1.mp4
    roi_coords = np.array([[282, 349], [219, 282]])  # [[411, 243], [472, 323]] for coin_test_1.mp4
    ref_n_frames = 2
    sos_n_frames = 4
    asos_train = 4
    asos_thr_factor = 5
    coin_thr = 20
    time_thr_coins = 20 # seconds

    roi_size = roi_coords[:, 1] - roi_coords[:, 0]
    asos_array = np.zeros(asos_train)
    reference = np.zeros(roi_size)
    ref_frames = np.zeros((roi_size[0], roi_size[1], ref_n_frames))
    sos_array = np.zeros(sos_n_frames)
    coin_times = np.zeros(nCoins)

    roi_counter = 0
    frame_counter = 0
    asos_train_counter = 0
    coin_frame = -1000
    asos_thr = 0
    coin_counter = 0
    mp_counter = 0
    r = []
    p = mp.Pool()
    # r = p.apply_async(utils.get_emotion, args=(filepath, emotion_key))

    init_time = time.time()
    this_init_time = init_time

    # Throw away the first frames
    for i in range(20):
        cap.read()

    expRunning = True
    while expRunning:

        if time.time() - init_time > time_thr_coins:
            break

        ret, frame = cap.read()
        if not ret:
            expRunning = False
            continue

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Motion Tracking here...

        # Emotion analysis
        if frame_counter % emotion_analysis_skip_frames == 0:
            utils.save_image(img)
            r.append(p.apply_async(utils.get_emotion, args=(filepath, emotion_key)))
            mp_counter = mp_counter + 1

        # Detect coin in ROI
        if frame_counter % 2 == 0:
            # Get roi and blur
            roi = img[roi_coords[0,0]:roi_coords[0,1], roi_coords[1,0]:roi_coords[1,1]]
            roi = cv2.GaussianBlur(roi, (13, 13), 0)

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

                            # Add timer
                            coin_times[coin_counter - 1] = time.time() - this_init_time
                            this_init_time = time.time()

            roi_counter = roi_counter + 1

            if DEBUG:
                cv2.imshow('image', img)
                cv2.waitKey(120)

        # Feed the image to sentiment analysis
        frame_counter = frame_counter + 1

    emotion_nr_coins = np.zeros(mp_counter)
    emotion_certainty_coins = np.zeros(mp_counter)
    for i in range(mp_counter):
        try:
            emotion_nr_coins[i], emotion_certainty_coins[i] = r[i].get()
        except:
            emotion_nr_coins[i], emotion_certainty_coins[i] = 0, 0
    p.close()
    p.join()

    print(coin_times)
    print(emotion_nr_coins)
    print(emotion_certainty_coins)

    utils.close_camera(cap)


if __name__ == '__main__':
    main()