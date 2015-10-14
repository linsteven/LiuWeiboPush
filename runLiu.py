#coding=utf-8
import getLiu
import time
import sendLiu

startHour = 7
stopHour = 21

sendLiu.informMyself('LiuWeiboPush启动')
while True :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/run_' + date + '.log','a')
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  logFile.write(str(hour) + ':' + str(minute) + '\n')
  logFile.close()
  enterLiu = False
  if hour >= startHour and hour < stopHour:
    enterLiu = True
    logFile = open('./log/run_' + date + '.log','a')
    logFile.write('\n\n\nEnterLiu\n\n')
    logFile.close()
    sendLiu.informMyself('开始大刘')
    #init getLiu
    sendedLst = getLiu.init(date)
    while(enterLiu) :
      getLiu.runOnce(sendedLst, date)
      h = time.localtime().tm_hour
      m = time.localtime().tm_min
      logFile = open('./log/run_' + date + '.log','a')
      logFile.write(str(h) + ':' + str(m) + '\n')
      if h == stopHour : # 22
        enterLiu = False
        sendLiu.informMyself('结束大刘')
      logFile.close()
      time.sleep(2) # 每2秒获取一次数据

  time.sleep(300)
#end while
