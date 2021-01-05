from python_speech_features import mfcc
from scipy.io import wavfile
from hmmlearn import hmm
import joblib
import os
import re
import numpy as np
def compute_mfcc(file):
    fs, audio = wavfile.read(file)
    mfcc_feat = mfcc(audio)
    return mfcc_feat
    
wavedict={}
labeldict={}
for root,dirs,files in os.walk('test_data'):
    for file in files:
        l=re.split('[_.]',file)
        wavedict[l[0]+'_'+l[1]]='test_data/'+file
        labeldict[l[0]+'_'+l[1]]=int(l[1])-1
print(wavedict)
print(labeldict)
#feat = compute_mfcc(wadict[wavid])
class Model():
    def __init__(self, CATEGORY=None, n_comp=3, n_mix = 3, cov_type='diag', n_iter=1000):
        super(Model, self).__init__()
        self.CATEGORY = CATEGORY
        self.category = len(CATEGORY)
        self.n_comp = n_comp
        self.n_mix = n_mix
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []
        for k in range(self.category):
            model = hmm.GMMHMM(n_components=self.n_comp, n_mix = self.n_mix,
                               covariance_type=self.cov_type, n_iter=self.n_iter)
            self.models.append(model)
    def train(self,wave=wavedict,label=labeldict):
        for x in wavedict:
            mfcc_feat = compute_mfcc(wave[x])
            self.models[label[x]].fit(mfcc_feat)
            
    def save(self, path="model.pkl"):
        joblib.dump(self.models,path)
    def load(self, path='model.pkl'):
        self.models = joblib.load(path)
    def test(self,filepath):
        result = []
        for k in range (self.category):
            model = self.models[k]
            mfcc_feat = compute_mfcc(filepath)
            rf = model.score(mfcc_feat)
            result.append(rf)
        print(result)
        result = np.array(result).argmax()
        return result
CATEGORY = ['open','close','twinkle','steady']
models = Model(CATEGORY=CATEGORY)
models.train()
models.save()
models.load()
for root,dirs,files in os.walk('test_data'):
    for file in files:
        ans = models.test('test_data/'+file)
        print(ans,file)
# models.test(wavdict=testdict, labeldict=testlabel)