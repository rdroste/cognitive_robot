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

    try:
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

        return main_emotion, emotions[main_emotion]

    except Exception as e:
        print(e.args)
        return 'Error', 'NA'





