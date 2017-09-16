from __future__ import print_function
import sounddevice as sd
import soundfile as sf
import os
from utils import *
from yumi_utils import *
import time

from bingtts import Translator

SAMPLERATE = 16000
NUMCHANNELS = 1
DURATION = 10


if __name__ == "__main__":

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

    # greetings from Yumi
    sd.play(hello_audio, SAMPLERATE, blocking=True)

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
    if confidence < 0.9:
        got_name = True
        # USE LUIS TO GET NAME!!!
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

    # first game rules (blocks)
    sd.play(first_audio, SAMPLERATE, blocking=True)

    # ROBOT MOVE
    # moveDoubleRobot('T_ROB_R','PegTest','T_ROB_L')
    time.sleep(5)

    # user turn
    sd.play(your_turn, SAMPLERATE, blocking=True)
    time.sleep(15)

    # great job
    sd.play(great_job, SAMPLERATE, blocking=True)
    # WITH NAME IF DETECTED!!
    time.sleep(2)

    # second game rules (coin test)
    sd.play(second_game, SAMPLERATE, blocking=True)

    # ROBOT MOVE
    # moveSingleRobot('T_ROB_R','CoinTest')
    time.sleep(5)

    # user turn
    sd.play(your_turn, SAMPLERATE, blocking=True)
    time.sleep(15)

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
    sentiment_score = get_sentiment_score(text)
    print("Sentiment score: ", sentiment_score)
    # positive = True

    # farewell
    if sentiment_score > 0.5:
        sd.play(pos_resp, SAMPLERATE, blocking=True)
    else:
        sd.play(neg_resp, SAMPLERATE, blocking=True)


    




