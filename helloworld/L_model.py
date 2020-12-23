from python_speech_features  import mfcc
import pyaudio
class YuYinShiBie():
    @staticmethod
    def compute_mfcc(wav):
        '''
        compute mfcc by wav
        '''
        mfcc_feat = mfcc(audio)
        return mfcc_feat
    @staticmethod
    def read_wav(file):
        '''
        read wav by file
        '''
        fs, audio = wavfile.read(file)
        return file

class Model():
    def __init__(self, CATEGORY=None, n_comp=12, n_mix=3, cov_type='diag', n_iter=1000):
        #why i need it?
        '''
        CATEGORY:所有标签的list
        n_comp:每个孤立词中的状态数 zzy感觉是3*音素
        n_mix：每个状态包含的混合高斯数量
        cov_type:协方差矩阵的类型
        n_iter:训练迭代次数
        '''
        super().__init__()
        self.CATEGORY = CATEGORY
        self.category = len(CATEGORY)
        self.n_comp = n_comp
        self.n_mix = n_mix
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []
        for k in range(self.category):
            model = hmm.GMMHMM(n_components = self.n_comp, n_mix = self.n_mix,
                                covariance_type = self.cov_type, n_iter = self.n_iter)
            self.models.append(model)
class Record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pyaudio.Pyaudio()
    @classmethod
    def record(cls):
        '''maybe'''
        stream = p.open(format=cls.FORMAT,channels=cls.CHANNELS,rate=cls.RATE,input=True,frames_perbuffer=cls.CHUNK)
    @classmethod
    def write_wav(cls,file,data):
        wf = wave.open(file,'wb')
        wf.setchannels(cls.CHANNELS)
        wf.setsampwidth(cls.p.get_sample_size(cls.FORMAT))
        wf.setframerate(cls.RATE)
        wf.writeframes(data)
