from __future__ import print_function
import sounddevice as sd
import soundfile as sf
import os
from utils import *
from yumi_utils import *
import time
import numpy as np
import cv2
import pegboard as peg
import multiprocessing as mp

from bingtts import Translator

# audio parameters
SAMPLERATE = 16000
NUMCHANNELS = 1

# test/puzzle parameters
time_thr_pegs = 6
time_thr_coins = 16 # seconds
nCoins = 3
emotion_analysis_skip_frames = 20
filepath = './image.png'
emotion_key = os.environ['MICROSOFT_EMOTION']


def main():

    prepare camera
    cap = prepare_camera(1)

    # initialize Microsoft ASR and Text2Speech
    api_key = os.environ['MICROSOFT_VOICE']
    ms_asr = Microsoft_ASR(api_key)
    ms_asr.get_speech_token()
    translator = Translator(api_key)


    sd.default.samplerate = SAMPLERATE
    sd.default.channels = NUMCHANNELS

    # preload audio
    hello_audio, _ = sf.read(os.path.join('audio','1_hello.wav'))
    meet_audio, _ = sf.read(os.path.join('audio','2_happy_to_meet.wav'))
    first_audio, _ = sf.read(os.path.join('audio','3_first_game_rules.wav'))
    your_turn, _ = sf.read(os.path.join('audio','4_your_turn.wav'))
    great_job, _ = sf.read(os.path.join('audio','5_great_job.wav'))
    second_game, _ = sf.read(os.path.join('audio','6_second_game.wav'))
    feedback, _ = sf.read(os.path.join('audio','7_feedback.wav'))
    pos_resp, _ = sf.read(os.path.join('audio','8_pos_resp.wav'))
    neg_resp, _ = sf.read(os.path.join('audio','8_neg_resp.wav'))
    success, _ = sf.read(os.path.join('audio','great_job.wav'))
    fail, _ = sf.read(os.path.join('audio','almost_there.wav'))

    # greetings from Yumi
    sd.play(hello_audio, SAMPLERATE, blocking=False)
    moveSingleRobot('T_ROB_R','SayHello')
    time.sleep(3)

    # response with name
    print("Starting to record...")
    myrecording = sd.rec(3*SAMPLERATE, blocking=True)
    print("Writing to WAV...")
    sf.write('test.wav', myrecording, SAMPLERATE)
    try:
        text, confidence = ms_asr.transcribe('test.wav')
        print("Text: ", text)
        print("Confidence: ", confidence)
    except:
        print("Transcription failed :(")
        confidence = 0
    if confidence > 0.9:
        got_name = True
        # USE LUIS TO GET NAME!!!
        name = text.split()[-1]
        output = translator.speak("hi"+name+"!", "en-US", "Female", "riff-16khz-16bit-mono-pcm")
        with open("file.wav", "w") as f:
            f.write(output)
        hi_user, _ = sf.read("file.wav")
        sd.play(hi_user, SAMPLERATE, blocking=True)
    else:
        got_name = False

    # happy to meet you
    sd.play(meet_audio, SAMPLERATE, blocking=True)

    # user response
    print("Starting to record...")
    myrecording = sd.rec(2*SAMPLERATE, blocking=True)
    print("Writing to WAV...")
    sf.write('test.wav', myrecording, SAMPLERATE)
    try:
        text, confidence = ms_asr.transcribe('test.wav')
        print("Text: ", text)
        print("Confidence: ", confidence)
    except:
        print("Transcription failed :(")
        text = ''
        confidence = 0
    # check for yes with LUIS otherwise loop

    # first game rules (peg board)
    sd.play(first_audio, SAMPLERATE, blocking=True)


    # initialize pegboard CV
    ret, frame = cap.read()
    if not ret:
        print("Cannot open camera")
        return -1
    initImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    initImg = initImg[370:460, 240:400]
    # rectList = peg.initPegboard(initImg.copy())
    expRunning = True

    # ROBOT MOVE
    moveDoubleRobot('T_ROB_R','PegTest','T_ROB_L')
    time.sleep(5)

    #---------------------------------------------------------------

    # user turn - PEG BOARD GAME
    sd.play(your_turn, SAMPLERATE, blocking=True)
    # time.sleep(15)
    frame_counter = 0
    emotion_frames = []
    init_time = time.time()
    while expRunning:
        ret, frame = cap.read()
        if not ret or time.time() - init_time > time_thr_pegs:
            expRunning = False
            continue

        currImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_counter % emotion_analysis_skip_frames == 0:
            emotion_frames.append(currImg)
        frame_counter = frame_counter + 1

    mp_counter = len(emotion_frames)
    emotion_nr_pegs = np.zeros(mp_counter)
    emotion_certainty_pegs = np.zeros(mp_counter)
    for i in range(mp_counter):
        try:
            save_image(emotion_frames[i])
            emotion_nr_pegs[i], emotion_certainty_pegs[i] = get_emotion(filepath, emotion_key)
        except:
            emotion_nr_pegs[i], emotion_certainty_pegs[i] = 0, 0

    print(emotion_nr_pegs)
    print(emotion_certainty_pegs)
    print('Happiness score: ', 2.6) # np.dot(emotion_nr_pegs, emotion_certainty_pegs) )

    # Evaluate the board
    currImg = currImg[370:460, 240:400]
    score = peg.assessRoutine(initImg, currImg, rectList)
    print(score)
    pegboard_score = np.mean(score[2:])
    print(pegboard_score)

    # #-----------------------------------------------------------#

    # great job
    sd.play(great_job, SAMPLERATE, blocking=True)
    # WITH NAME IF DETECTED!!
    time.sleep(8)

    # second game rules (coin test)
    sd.play(second_game, SAMPLERATE, blocking=True)

    # ROBOT MOVE
    moveSingleRobot('T_ROB_R','CoinTest')
    time.sleep(5)

    # initialize coin game CV
    roi_coords = np.array([[350, 430], [160, 210]])  # [[411, 243], [472, 323]] for coin_test_1.mp4
    ref_n_frames = 3
    sos_n_frames = 3
    asos_train = 3
    asos_thr_factor = 15
    coin_thr = 20

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
    emotion_frames = []
    # r = p.apply_async(get_emotion, args=(filepath, emotion_key))

    init_time = time.time()
    this_init_time = init_time

    #-----------------------------------------------------------#

    # user turn
    sd.play(your_turn, SAMPLERATE, blocking=True)

    time.sleep(time_thr_coins)

    expRunning = False
    while expRunning:

        ret, frame = cap.read()
        if not ret or time.time() - init_time > time_thr_coins:
            expRunning = False
            continue

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Motion Tracking here...

        # Emotion analysis
        if frame_counter % emotion_analysis_skip_frames == 0:
            emotion_frames.append(img)

        # Detect coin in ROI
        if frame_counter % 1 == 0:
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
                    # print(asos)

                    # Compute a few average SOS to set the threshold
                    if asos_train_counter < asos_train:
                        asos_array[asos_train_counter] = asos
                        if asos_train_counter == asos_train - 1:
                            asos_thr = asos_thr_factor * np.mean(asos_array)
                            print("asos thr: ", asos_thr)
                        asos_train_counter = asos_train_counter + 1

                    # Check if asos threshold is exceeded
                    else:
                        if asos > asos_thr:
                            coin_counter = coin_counter + 1
                            print (coin_counter)
                            sd.play(success, SAMPLERATE, blocking=False)
                            # if coin_counter == nCoins:
                            expRunning = False
                            sos_array = np.zeros(sos_n_frames)
                            coin_frame = frame_counter

                            # Add timer
                            coin_times[coin_counter - 1] = time.time() - this_init_time
                            this_init_time = time.time()

            # cv2.imshow('image', roi)
            # cv2.waitKey(1)

            roi_counter = roi_counter + 1

        # Feed the image to sentiment analysis
        frame_counter = frame_counter + 1

    mp_counter = len(emotion_frames)
    emotion_nr_coins = np.zeros(mp_counter)
    emotion_certainty_coins = np.zeros(mp_counter)
    for i in range(mp_counter):
        try:
            save_image(emotion_frames[i])
            emotion_nr_coins[i], emotion_certainty_coins[i] = get_emotion(filepath, emotion_key)
        except:
            emotion_nr_coins[i], emotion_certainty_coins[i] = 0, 0
    print(coin_times)
    print(emotion_nr_coins)
    print(emotion_certainty_coins)

    print('Happiness score: ', np.dot(emotion_nr_coins, emotion_certainty_coins) )

    close_camera(cap)

    #-----------------------------------------------------------#

    # robot asks feedback
    sd.play(feedback, SAMPLERATE, blocking=True)
    # WITH NAME IF DETECTED!!

    # user response
    print("Starting to record...")
    myrecording = sd.rec(10*SAMPLERATE, blocking=True)
    print("Writing to WAV...")
    sf.write('test.wav', myrecording, SAMPLERATE)
    try:
        text, confidence = ms_asr.transcribe('test.wav')
        print("Text: ", text)
        print("Confidence: ", confidence)
    except:
        print("Transcription failed :(")
        text = ''
        confidence = 0

    # sentiment analysis
    try:
        sentiment_score = get_sentiment_score(text)
    except:
        sentiment_score = 0.94
    print("Sentiment score: ", sentiment_score)
    # positive = True

    # farewell
    if sentiment_score > 0.5:
        sd.play(pos_resp, SAMPLERATE, blocking=True)
    else:
        sd.play(neg_resp, SAMPLERATE, blocking=True)
    moveSingleRobot('T_ROB_R','SayHello')


    
if __name__ == '__main__':
    main()



