# Cognitive Robot

Cognitive robot to diagnose disorders of motor skills and coordination in children

## Inspiration
Many children suffer from Developmental Coordination Disorder (DCD), a motor skill disorder that affects 5 to 6% of all school aged children<sup>1</sup>. The affected children have difficulties performing everyday tasks and therefore suffer from significant impairment of their quality of life. However, DCD is difficult to diagnose since, by definition, it is not linked to any identifiable medical of neurological disorders. Therefore, designing accurate methods for diagnosing the disorders are crucial.


## What It Does
The JRED team set out to combine a high-tech robot with state-of-the-art computer cognition to potentially revolutionize the diagnosis of DCD. While traditional methods are conducted by pen and paper, we offer more quantitative metrics, a standardized test allowing for consistent results, and an innovative human-robot-computer interface to allow for a stress-free experience for the child.

Our tests are inspired by standart test, such as the ABC test<sup>2</sup> and the Purdue Pegboard Test<sup>3</sup>

<sub><sup>1 https://canchild.ca/en/diagnoses/developmental-coordination-disorder</sup></sub>
<sub><sup>2 http://www.rehabmeasures.org/Lists/RehabMeasures/DispForm.aspx?ID=1144</sup></sub>
<sub><sup>3 http://www.pearsonclinical.com/therapy/products/100000433/movement-assessment-battery-for-children-second-edition-movement-abc-2.html</sup></sub>

## The Tech
The ABB YuMi is a collaborative dual-arm robot is used to show the child the tasks to be performed in an accurate and reproducible manner.
A laptop's microphone and speakers serve as the "mouth" and "ears for YuMi. The following Python packages are used for audio capture, saving, and playback: `sounddevice` and `soundfile`.

A Logitech webcam is used to give YuMi sight. The OpenCV library is used to perform standard image analysis and processing techniques such as convolution, de-convolution, spatial filtering, segmentation, and blob detection.

Finally, the following Microsoft Azure services were used to give YuMi cognitive abilities:

1. Bing Speech API for speech-to-text and text-to-speech.
2. Emotion API for analyzing the behavior of the participant during each exercise.
3. Text Analytics API for sentiment analysis during the participants final self-reflection.

