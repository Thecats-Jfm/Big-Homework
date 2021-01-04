import threading
import time

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
            Libs.Output('timer_end.wav')
