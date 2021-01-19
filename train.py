import os
import re

import joblib
import numpy as np
from hmmlearn import hmm
from python_speech_features import mfcc
from scipy.io import wavfile


def compute_mfcc(file):
    fs, audio = wavfile.read(file)
    mfcc_feat = mfcc(audio)
    return mfcc_feat


wavedict = {}
labeldict = {}
st = {'exit': 0, '5min': 1, '1min': 2, 'pause': 3,
      'resume': 4, 'howlong': 5, 'stop': 6, 'Intem': 7, 'Tem': 8}
for root, dirs, files in os.walk('train'):
    for file in files:
        l = re.split('[.]', file)
        tag_ = l[0]
        if(tag_[len(tag_)-1] == '0'):
            tag = tag_[:len(tag_)-2]
        else:
            tag = tag_[:len(tag_)-1]
        wavedict[tag_] = 'train/'+file
        labeldict[tag_] = st[tag]
print(wavedict)
print(labeldict)
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

    def train(self, wave=wavedict, label=labeldict):
        for x in wavedict:
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


models = Model(CATEGORY=CATEGORY)
models.train()
models.save()
models.load()
for wave in wavedict:
    ret = models.test(wavedict[wave])
    if(ret != labeldict[wave]):
        print(wave, ret)
