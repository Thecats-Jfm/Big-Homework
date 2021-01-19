import pyaudio
import wave
import RPi.GPIO as GPIO
import time
KEY = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN,GPIO.PUD_UP)
def record_audio(wave_out_path,record_second):
    print(wave_out_path)
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    while True:
        if GPIO.input(KEY)==1:
            time.sleep(0.1)
        else:
            break
    stream = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)
    wf = wave.open(wave_out_path,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("* recording")
    st=time.time()
    for i in range(0,int(RATE / CHUNK * record_second)):
        data = stream.read(CHUNK)
        wf.writeframes(data)
        if(GPIO.input(KEY)==1):
            break;
    et=time.time()
    print("* done recording")
    print("Recorded for %fs"%(et-st))
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

id_ = 0
tag = 'pause'
try:
    while(True):
        id_ += 1
        record_audio("train/"+tag+ str(id_) +".wav",1000)
        time.sleep(1.5)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
print("End")