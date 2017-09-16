# https://codeplasma.com/2012/12/03/getting-webcam-images-with-python-and-opencv-2-for-real-this-time/

import cv2
import httplib, urllib, base64, sys, json
import operator

# Captures a single image from the camera and returns it in PIL format
def get_image(camera):
    _, im = camera.read()
    return im

# returns camera object
def prepare_camera(port=0, prep_frames=30):

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




