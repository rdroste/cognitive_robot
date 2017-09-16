from __future__ import print_function
import sounddevice as sd
import soundfile as sf
import os
from utils import *

from bingtts import Translator

SAMPLERATE = 16000
NUMCHANNELS = 1
DURATION = 10


def speak_to_YuMi():

    try:
        print("Starting to record...")
        myrecording = sd.rec(DURATION*SAMPLERATE, blocking=True)
        print("Writing to WAV...")
        sf.write('test.wav', myrecording, SAMPLERATE)
    except:
        print("Recording failed :(")
        return

    try:
        text, confidence = ms_asr.transcribe('test.wav')
        print("Text: ", text)
        print("Confidence: ", confidence)
    except:
        print("Transcription failed :(")
        return

    # parse text
    if 'coin' in text:
        print("Doing the coin test...")
    elif 'block' in text:
        print("Doing the block test...")
    elif 'bye' in text:
        print("Waving to the audience...")
    else:
        print("I'm sorry, I didn't quite get that")


    output = translator.speak("This is a text to speech translation", "en-US", "Female", "riff-16khz-16bit-mono-pcm")



if __name__ == "__main__":

    # initialize Microsoft ASR and Text2Speech
    api_key = os.environ['MICROSOFT_VOICE']
    ms_asr = Microsoft_ASR(api_key)
    ms_asr.get_speech_token()
    translator = Translator(api_key)


    sd.default.samplerate = SAMPLERATE
    sd.default.channels = NUMCHANNELS

    # always listening
    while(1):
        # ideally trigger word for this
        print("\nWhat would you like to do?")
        print("[1] - Tell YuMi to do something")
        print("[2] - QUIT")
        print("Enter your choice [1-2]: ", end="")
        choice = int(input())

        if choice == 1:
            speak_to_YuMi()
        elif choice == 2:
            os.remove('test.wav')
            break
        else:
            print("Invalid choice!")



