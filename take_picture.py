from utils import *
import os

filename = 'test_image.jpg'
emotion_key = os.environ['MICROSOFT_EMOTION']

# get image
camera = prepare_camera()
im = get_image(camera)
save_image(im, filename)
close_camera(camera)

# get main emotion and score
filepath = os.path.join(os.getcwd(), filename)
emotion, score = get_emotion(filepath, emotion_key)
print('Detected emotion: ', emotion)
print('Score: ', score)


