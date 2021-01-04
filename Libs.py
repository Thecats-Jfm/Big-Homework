# coding = utf-8
import json
import sys
from urllib.error import URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

from playsound import playsound

# 调用百度语音合成api
API_KEY = '2l75V5XghS281dcwKmgGvkpR'
SECRET_KEY = 'n2AwmvQxuQ68oQWCYAgz0feyrN8iOOp4'
# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 0
SPD = 4  # 语速，取值0-15，默认为5中语速
PIT = 5  # 音调，取值0-15，默认为5中语调
VOL = 8  # 音量，取值0-9，默认为5中音量
AUE = 6  # 文件格式相关.wav
FORMAT = 'wav'  # 下载的文件格式

CUID = "123456PYTHON"
TTS_URL = 'http://tsn.baidu.com/text2audio'
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 语音合成tag
nid = 0

class DemoError(Exception):  # 错误类
    pass


def fetch_token():  # 生成token
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError(
            'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def Baidu_TTS(TEXT):  # 根据TEXT生成result.wav
    global nid
    nid += 1
    token = fetch_token()
    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
    data = urlencode(params)
    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        headers = dict((name.lower(), value)
                       for name, value in f.headers.items())
        has_error = ('content-type' not in headers.keys()
                     or headers['content-type'].find('audio/') < 0)
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True
    save_file = "error.txt" if has_error else '.\\wav\\temp\\result'+str(nid)+'.' + FORMAT
    with open(save_file, 'wb') as of:
        of.write(result_str)
    if has_error:
        result_str = str(result_str, 'utf-8')
        print("tts api error:" + result_str)
    print("result saved as :" + save_file)


def Act():
    id = int(input())
    return id


wav_path = '.\\wav\\'


def Output(Path):  # 从wav文件夹下输出
    playsound(wav_path+Path)


def OutputText(Text):  # 通过百度TTS生成wav并输出
    global nid
    Baidu_TTS(Text)
    path = 'temp\\result'+str(nid)+'.wav'
    Output(path)
