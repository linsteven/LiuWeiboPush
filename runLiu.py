#coding=utf-8
import getLiu
import time
from random import randint
from log import LogRun

startHour = 7
stopHour = 21

LogRun('LiuWeiboPush启动')

while True :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  LogRun(str(hour) + ':' + str(minute))
  enterLiu = False
  if hour >= startHour and hour < stopHour:
    enterLiu = True
    LogRun('\nEnterLiu 开始大刘')
    sendedLst = getLiu.init()
    while(enterLiu) :
      getLiu.runOnce(sendedLst)
      h = time.localtime().tm_hour
      m = time.localtime().tm_min
      LogRun(str(h) + ':' + str(m))
      if h == stopHour : # 22
        enterLiu = False
        LogRun('结束大刘\n')
      time.sleep(randint(1,3)) # 每1-3秒获取一次数据

  time.sleep(300)
#end while
