import glob
import time
import core
import RPi.GPIO as GPIO
import Libs

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
    core.T.exit_flag =True
    print('stop by key')
