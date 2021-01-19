import glob
import os
import time
import wave

import core
import joblib
import numpy as np
import pyaudio
import RPi.GPIO as GPIO
from hmmlearn import hmm
from python_speech_features import mfcc
from scipy.io import wavfile

import Class
import Libs

KEY = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN, GPIO.PUD_UP)


def Finish():  # 每次结束程序释放GPIO控制
    GPIO.cleanup()


class Temperature:  # 利用树莓派上的温度传感器获取室温
    @staticmethod
    def temperature():
        name = glob.glob('/sys/bus/w1/devices/28-*')
        f = open(name[0] + '/w1_slave', 'r')
        lines = f.readlines()
        f.close()
        temperature = float(lines[1][-6:-1])/1000
        return temperature


def compute_mfcc(file):
    fs, audio = wavfile.read(file)
    mfcc_feat = mfcc(audio)
    return mfcc_feat


models = Class.Model(CATEGORY=Class.CATEGORY)  # 装载训练好的模型
models.load()


def record_test(wave_out_path, record_second):  # 计算输入语音对应的最大可能概率的文字
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
    if(et-st < 0.4):  # 若录音时间过短，不处理
        opt = -1
    else:
        opt = models.test(wave_out_path)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    return opt
