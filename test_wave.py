import os
from utils import *
from yumi_utils import *
import time
import numpy as np
import cv2
import pegboard as peg
import multiprocessing as mp


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

	moveDoubleRobot('T_ROB_R','PegTest','T_ROB_L')
    time.sleep(5)


if __name__ == '__main__':
    main()