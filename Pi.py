import glob
import os
import time
import wave

import joblib
import numpy as np
import pyaudio
import RPi.GPIO as GPIO
from hmmlearn import hmm
from python_speech_features import mfcc
from scipy.io import wavfile

import core
import Libs
import Class

KEY = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(KEY, GPIO.FALLING, callback=mcb, bouncetime=200)


def Finish():
    GPIO.cleanup()


class Temperature:
    @staticmethod
    def temperature():
        name = glob.glob('/sys/bus/w1/devices/28-*')
        f = open(name[0] + '/w1_slave', 'r')
        lines = f.readlines()
        f.close()
        temperature = str(float(lines[1][-6:-1])/1000)
        return temperature


def mcb(ch):  # MyCallBack
    core.T.exit_flag = True
    print('stop by key')


def compute_mfcc(file):
    fs, audio = wavfile.read(file)
    mfcc_feat = mfcc(audio)
    return mfcc_feat



models = Model(CATEGORY=CATEGORY)
models.load()

def record_audio(wave_out_path, record_second):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    while True:
        if GPIO.input(KEY) == 1:
            time.sleep(0.1)
        else:
            break
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("* recording")
    st = time.time()
    for i in range(0, int(RATE / CHUNK * record_second)):
        data = stream.read(CHUNK)
        wf.writeframes(data)
        if(GPIO.input(KEY) == 1):
            break
    et = time.time()
    print("* done recording")
    print("Recorded for %fs" % (et-st))
    opt = Class.models.test('test.wav')
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    return opt


try:
    while(True):
        record_audio("test.wav", 1000)
except KeyboardInterrupt:
    pass
