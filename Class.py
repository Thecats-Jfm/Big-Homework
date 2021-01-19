import threading
import time

import joblib
import numpy as np
from hmmlearn import hmm
from python_speech_features import mfcc
from scipy.io import wavfile

import Libs
import Ways


class myThread(threading.Thread):  # 自己编写的myThread类，支持暂停，继续，终止线程的操作
    def __init__(self, act, exit):  # 初始化线程
        threading.Thread.__init__(self)
        self.__flag = threading.Event()  # 终止标志
        self.__flag.set()
        self.__running = threading.Event()  # 暂停标志
        self.__running.set()
        self.act = act  # 线程重复运行的函数
        self.exit = exit  # 线程退出时运行的函数

    def pause(self):  # 暂停线程
        self.__flag.clear()

    def resume(self):  # 继续线程
        self.__flag.set()

    def stop(self):  # 终止线程
        self.__flag.set()
        self.__running.clear()

    def run(self):  # 运行线程
        while self.__running.isSet():
            self.__flag.wait()
            if(self.act()):
                pass
            else:
                self.exit()
                self.stop()


class Timer():  # 计时器类，支持覆盖计时器，设定计时时间，开始、暂停计时，查看剩余时间的操作。
    def __init__(self):
        self.time = -1

    def Start(self, times):  # 开始计时
        self.time = times  # 设定秒数
        self.exit_flag = False  # 计时器启用标志
        if hasattr(self, 'Thread'):  # 计时器覆盖
            print("Stop old thread.")
            self.Thread.stop()
        self.Thread = myThread(self.count, self.exit)
        self.Thread.start()

    def Pause(self):  # 暂停
        self.Thread.pause()

    def Resume(self):  # 继续
        self.Thread.resume()

    def Showtime(self):  # 查看剩余时间并语音播报
        s = '计时器剩余'
        m = self.time//60
        if(m > 0):
            s += str(m)+'分钟'
        s += str(self.time % 60)+'秒'
        Libs.OutputText(s)

    def Stop(self):  # 停止
        self.Thread.stop()

    def count(self):  # 计时器线程中运行的计时函数
        if(self.time > 0):
            time.sleep(1)
            self.time = self.time - 1
        return self.time

    def exit(self):  # 计时器线程的终止函数
        for i in range(100):
            if self.exit_flag:
                break
            time.sleep(1.5)
            Libs.Output('timer_end.wav')


CATEGORY = ['exit', '5min', '1min', 'pause',
            'resume', 'howlong', 'stop', 'Intem', 'Tem']

class Model():#GMM-HMM模型
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
