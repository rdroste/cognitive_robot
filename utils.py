# https://codeplasma.com/2012/12/03/getting-webcam-images-with-python-and-opencv-2-for-real-this-time/

import cv2
import httplib, urllib, base64, sys, json
import operator
import os
import uuid, requests


# Captures a single image from the camera and returns it in PIL format
def get_image(camera):
    _, im = camera.read()
    return im

# returns camera object
def prepare_camera(port=1, prep_frames=30):

    camera = cv2.VideoCapture(port)

    # Ramp the camera - these frames will be discarded and are only used to allow v4l2 to adjust light levels, if necessary
    for i in range(prep_frames):
        _ = get_image(camera)

    return camera

# save image
def save_image(camera_capture, filename='image.png'):
    cv2.imwrite(filename, camera_capture)


# close camera
def close_camera(camera):
    camera.release()
    del(camera)
    cv2.destroyAllWindows()


# get emotions
def get_emotion(filepath, api_key):

    print("here")

    headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': api_key}

    params = urllib.urlencode({})

    body = open(filepath,'rb').read()

    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)

    response = conn.getresponse()
    data = response.read()
    json_data = json.loads(data.decode('utf-8'))

    # POS : anger, contempt, disgust, fear, sadness
    # NEG : happiness, neutral, surprise
    emotions = json_data[0]['scores']
    # print(emotions)

    # print(emotions)
    main_emotion = max(emotions, key=lambda key: emotions[key])

    conn.close()

    if (main_emotion == "anger" or main_emotion == "contempt" or main_emotion == "disgust" or main_emotion == "fear"
        or main_emotion == "sadness"):
        main_emotion_nr = 1
    elif main_emotion == "neutral" or main_emotion == "surprise":
        main_emotion_nr = 2
    elif main_emotion == "happiness":
        main_emotion_nr = 3
    else:
        main_emotion_nr = 0

    print(main_emotion)

    return main_emotion_nr, emotions[main_emotion]



# voice interactions
class Microsoft_ASR():
    def __init__(self, api_key):
        self.sub_key = api_key
        self.token = None
        pass

    def get_speech_token(self):
        FetchTokenURI = "/sts/v1.0/issueToken"
        header = {'Ocp-Apim-Subscription-Key': self.sub_key}
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        body = ""
        conn.request("POST", FetchTokenURI, body, header)
        response = conn.getresponse()
        str_data = response.read()
        conn.close()
        self.token = str_data
        print("Got Token: ", self.token)
        return True

    def transcribe(self,speech_file):

        # Grab the token if we need it
        if self.token is None:
            print("No Token... Getting one")
            self.get_speech_token()

        endpoint = 'https://speech.platform.bing.com/recognize'
        request_id = uuid.uuid4()
        # Params form Microsoft Example 
        params = {'scenarios': 'ulm',
                  'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
                  'locale': 'en-US',
                  'version': '3.0',
                  'format': 'json',
                  'instanceid': '565D69FF-E928-4B7E-87DA-9A750B96D9E3',
                  'requestid': uuid.uuid4(),
                  'device.os': 'linux'}
        content_type = "audio/wav; codec=""audio/pcm""; samplerate=16000"

        def stream_audio_file(speech_file, chunk_size=1024):
            with open(speech_file, 'rb') as f:
                while 1:
                    data = f.read(1024)
                    if not data:
                        break
                    yield data

        headers = {'Authorization': 'Bearer ' + self.token, 
                   'Content-Type': content_type}
        resp = requests.post(endpoint, 
                            params=params, 
                            data=stream_audio_file(speech_file), 
                            headers=headers)
        val = json.loads(resp.text)
        return val["results"][0]["name"], val["results"][0]["confidence"]






