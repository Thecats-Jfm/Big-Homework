#这里要作为一个自动机的核心
import threading
import time
import Ways
import Libs
from Class import Timer
def A():
    pass
def B():
    pass
def C():
    pass







# Libs.Baidu_YuYinHeCheng(TEXT)
# exit()


if __name__ == "__main__":
    T = Timer()
    while True:
        act_id = Libs.Act()
        if act_id == 1: #计时五分钟
            T.Start(5*60)
        elif act_id == 2: #计时一分钟
            T.Start(1*60)
        elif act_id == 3: #暂停计时
            T.Pause()
        elif act_id == 4: #继续计时
            T.Resume()
        elif act_id == 5: #计时器还剩多久
            T.Showtime()
        elif act_id == 6: #停止计时
            T.Stop()
        elif act_id == 7: #现在的室温是几度
            pass
        elif act_id == 8: #今天天气怎么样
            pass
        elif act_id == 0: #退出
            pass
