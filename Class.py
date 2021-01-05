import threading
import time

import joblib
import numpy as np
from hmmlearn import hmm
from python_speech_features import mfcc
from scipy.io import wavfile

import Libs
import Ways


class myThread(threading.Thread):
    def __init__(self, act, exit):
        threading.Thread.__init__(self)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.act = act
        self.exit = exit

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            if(self.act()):
                pass
            else:
                self.exit()
                self.stop()


class Timer():
    def __init__(self):
        self.time = -1

    def Start(self, times):
        self.time = times
        self.exit_flag = False
        if hasattr(self, 'Thread'):
            print("Stop old thread.")
            self.Thread.stop()
        self.Thread = myThread(self.count, self.exit)
        self.Thread.start()

    def Pause(self):
        self.Thread.pause()

    def Resume(self):
        self.Thread.resume()

    def Showtime(self):
        s = '计时器剩余'
        m = self.time//60
        if(m > 0):
            s += str(m)+'分钟'
        s += str(self.time % 60)+'秒'
        Libs.OutputText(s)

    def Stop(self):
        self.Thread.stop()

    def count(self):
        if(self.time > 0):
            time.sleep(1)
            self.time = self.time - 1
        print(self.time)
        return self.time

    def exit(self):
        for i in range(100):
            if self.exit_flag:
                break
            time.sleep(1.5)
            Libs.Output('timer_end.wav')


CATEGORY = ['exit', '5min', '1min', 'pause',
            'resume', 'howlong', 'stop', 'Intem', 'Tem']


class Model():
    def __init__(self, CATEGORY=None, n_comp=3, n_mix=3, cov_type='diag', n_iter=1000):
        super(Model, self).__init__()
        self.CATEGORY = CATEGORY
        self.category = len(CATEGORY)
        self.n_comp = n_comp
        self.n_mix = n_mix
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []
        for k in range(self.category):
            model = hmm.GMMHMM(n_components=self.n_comp, n_mix=self.n_mix,
                               covariance_type=self.cov_type, n_iter=self.n_iter)
            self.models.append(model)

    def train(self, wave, label):
        for x in waved:
            mfcc_feat = compute_mfcc(wave[x])
            self.models[label[x]].fit(mfcc_feat)

    def save(self, path="model.pkl"):
        joblib.dump(self.models, path)

    def load(self, path='model.pkl'):
        self.models = joblib.load(path)

    def test(self, filepath):
        result = []
        for k in range(self.category):
            model = self.models[k]
            mfcc_feat = compute_mfcc(filepath)
            rf = model.score(mfcc_feat)
            result.append(rf)
        result = np.array(result).argmax()
        return result
