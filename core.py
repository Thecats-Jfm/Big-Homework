# 这里要作为一个自动机的核心
import threading
import time
import Ways
import Libs
import Pi
from Class import Timer

T = Timer()
# Libs.Baidu_YuYinHeCheng(TEXT)
# exit()
if __name__ == "__main__":

    while True:
        act_id = Libs.Act()
        if act_id == 1:  # 计时五分钟
            T.Start(5*60)
            Libs.Output('5min_start.wav')

        elif act_id == 2:  # 计时一分钟
            T.Start(1*60)
            Libs.Output('1min_start.wav')
        elif act_id == 3:  # 暂停计时
            T.Pause()
            Libs.Output('timer_pause.wav')
        elif act_id == 4:  # 继续计时
            T.Resume()
            Libs.Output('timer_continue.wav')
        elif act_id == 5:  # 计时器还剩多久
            T.Showtime()
        elif act_id == 6:  # 停止计时
            T.Stop()
            Libs.Output('timer_exit.wav')
        elif act_id == 7:  # 现在的室温是几度
            t = Pi.Temperature.temperature()
            print('现在的室温是%.2lf°C'%t)
            Libs.OutputText('现在的室温是%.2lf°C'%t)
        elif act_id == 8:  # 今天天气怎么样
            Libs.Output('wait.wav')
            Libs.OutputText(Libs.Get_Weather())
        elif act_id == 0:  # 退出
            Libs.Output('goodbye.wav')
            Pi.Finish()
            exit()
        else :
            pass
