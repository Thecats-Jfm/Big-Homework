# Big-Homework
meow~

2020/12/23
现在整理一下想法并推进
首先我们要做的是一个智能语音助手
Passby

# 基础功能
1.支持语音输入
2.设计一个有限状态自动机，使得程序在自动机上运行 bingo~

## 3.支持语音输出 bingo~

接口：Libs.BaiDu_YuYinHeCheng(text) 会生成一个result.wav


# 附加功能
这部分为自动机状态
感觉还是可以做的。 可以讲讲比直接做
感觉还是不做了
这个用户体验并不好
## 计时5分钟
## 计时1分钟
支持计时器覆盖
支持暂停

## 暂停计时
## 继续计时
## 计时器还剩多久
## 停止计时
## 再见
## 现在室温是几度
## 今天天气怎么样



## 1.初始状态：默认待机 （低功耗） 不然直接一直切片吧 （一定时间后如果没有操作则回复）
。。不太会做。。还是改成了按键激活吧。。 参考之前按键的做法吧。

2.气温感知功能，感知室内温度（）抄原来的代码
3.天气预报功能，联网获取天气*（期待能给出着装建议and更多信息）http://www.tianqiapi.com/
4.计时器功能。调用多线程。


# 可拓展模块（？Idontknow）

4.（获取课表功能）
5.（拍照call小冰）（如果不好实现则算了）
6.憨批每日一句*（中二病也喜欢你）

# 日程
12.23 这一周起码吧按键输入做完，搭起有限状态自动机的架构，完善各个小功能。
12.23 我永远喜欢yyd
12.23 多线程测试