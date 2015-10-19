#coding: utf-8
import sys
import urllib
import re
import time
import codecs
import sendCloud
import socket
from log import LogError
from log import LogGet
from log import LogSended
from log import LogGetSended

#getHtml(url) 获取url对应的网页内容
#getWeibo 解析url获取微博内容、时间
#getNewWeibo 组合内容、时间，形成完整的微博，新微博则返回
#init  初始化每天的sendedLiu文件，以及sendedLst
#runOnce 每次运行，看是否获取新微博，获取成功则发邮件推送

socket.setdefaulttimeout(5)
weiboUrl = 'http://www.imaibo.net/index.php?app=home&mod=Space&act=getSpaceWeibo300&uid=1954702'

def getHtml(url) :
  html = ''
  try :
    page = urllib.urlopen(url)
    html = page.read()
  except IOError, e : #socket.error:
    errno,errstr = sys.exc_info()[:2]
    curtime = time.strftime('%H:%M:%S',time.localtime(time.time()))
    LogError('\n-----------------\n' + curtime)
    if errno == socket.timeout :
      LogError('There was a timeout')
    else :
      LogError('Some other socket error')
  return html

def getWeibo() :
  weiboLst = list()
  urlLst = list()
  weibos = getHtml(weiboUrl)
  if weibos == '' :
    return weiboLst, urlLst
  lines = weibos.split('\u')
  content = ''
  #转unicode为中文
  for word in lines : 
    if len(word) == 4 :
      content += unichr(int(word,16))
    elif re.match(r"^[a-f0-9]{4}", word) :
      word = word.replace('\/', '/')
      word = word.replace('''\\\"''','''"''')
      content += unichr(int(word[:4],16)) + word[4:]
    else :
      content += word
  #去除各种html标签等无用信息，提取微博内容及时间信息
  for line in content.split('</div>') :
    if len(line) > 0 :
      if u'刘鹏程SaiL直播' in line :
        pos = line.find(u'[刘鹏程SaiL直播]')
        line = line[pos:]
        pos = line.find(u'[刘鹏程SaiL直播]', 1,-1)
        if pos > 0 : # if the line contains '展开更多', remove the less one
          line = line[:pos]
        pos = line.find('</span><div')
        if pos > 0 :
          line = line[:pos]
        line = line.replace(u'[刘鹏程SaiL直播]</a>',u'[刘鹏程SaiL直播]')
        line = line.replace('<div>','')
        line = line.replace('</p>','')
        #LogGet(line)
       ### line, num = re.subn(ur"<((?!>).)*>", "", line)
        #line, num = re.subn(r'<a href.*_blank\'>','',line)
        #line, num = re.subn(r'<a target.*class\">','',line)
        #line, num = re.subn(r'<a target.*portfolio\/\d{2,6}\">','',line)
        #line, num = re.subn(r'<.*>','',line) # this line must be the last
        weiboLst.append(line)
      elif re.match(ur"^.*\d{2}:\d{2}.*$", line) or re.match(ur"^.*\d{1,2}分钟.*$", line)  or re.match(ur"^.*\d{1,2}秒.*$", line) :
        if u'原文评论' in line : #1、获取原文链接url(暂时没用) 2、获取时间ctime
          pos = line.find('<cite><a href')
          line = line[pos + 5:]
          pleft = line.find('http')
          pright = line.find('\"target')
          url = line[pleft:pright]
          #print url
          pos = line.find('blank\">')
          line = line[pos+7:]
          ctime, num = re.subn(r'<.*>','',line) # this line must be the last
          weiboLst.append(ctime) #暂时忽略url
        else : 
          pos = line.find(u'评论')
          line = line[pos:]
          pos = line.find('<a href')
          line = line[pos + 5:]
          pleft = line.find('http')
          pright = line.find('\"target')
          url = line[pleft:pright]
          pos = line.find('blank\">')
          line = line[pos+7:]
          ctime, num = re.subn(r'<.*>','',line) # this line must be the last
          weiboLst.append(ctime)
          urlLst.append(url)
      elif u"回复" in line : #当回复置顶时，不会有[刘鹏程SaiL直播], 需特殊处理
        pos1 = line.find(u'回复')
        part = line[pos1+1:]
        pos2 = part.find(u'回复')
        if pos2 > 0 :
          line = line[:pos2]
        line = line[pos1:]
        line = u'[刘鹏程SaiL直播]' + line
        line, num = re.subn(ur"<((?!>).)*>", "", line)
        weiboLst.append(line)
  #weiboLst中是微博内容及其时间，需要将其组合
  return weiboLst, urlLst

def combine() :
  #测试函数
  lst,urlLst = getWeibo()
  weibos = list()
  length = len(lst)
  #pos = lst[0].find(u'直播]')
  pos = 11 # pos+3 == 11
  for i in range(length) :
    if u'[刘鹏程' in lst[i] :
      weibo = lst[i]
      if u'[刘鹏程' in lst[i+1] :
        lst[i+1] = lst[i+1][11:]#去头部
        weibo += '(' + lst[i+2] + ')'
        weibo += u'//原文: ' + lst[i+1]
        weibo += '(' + lst[i+3] + ')'
        i += 3
      else : #没有原文，非转发，单条微博
        weibo += '(' + lst[i+1] + ')'
        i += 1
      #print i, weibo
      weibos.append(weibo)
  return weibos

def getNewWeibo(sendedLst) :
  lst,urlLst = getWeibo()
  length = len(lst)
  pos = 11 #去掉[刘鹏程Sail直播]
  weibo = ''
  url = ''
  hasNew = False
  cur = ''
  date = ''
  count = 0
  for i in range(12 if length > 12 else length):
    if u'[刘鹏程' in lst[i] :
      cur = lst[i]
      weibo = ''
      if u'[刘鹏程' in lst[i+1] :#有转发，原文内容
        lst[i+1] = lst[i+1][11:]#去头部
        weibo += lst[i] + '(' + lst[i+3] + ')'
        weibo += u'//原文: ' + lst[i+1]
        weibo += '(' + lst[i+2] + ')'
        i += 3
      else : #没有原文，非转发，单条微博
        weibo += lst[i] + '(' + lst[i+1] + ')'
        i += 1
      if cur not in sendedLst :
        #更新sendedLst，并保持不是很大,10--20
        hasNew = True
        sendedLst.insert(0, cur)
        if len(sendedLst) >= 20 :
          for k in range(10) :
            sendedLst.pop()
        LogSended(cur)#更新本地文件
        url = urlLst[count]
        break  #一次假设只有一条更新，即5秒内大刘不会发两条微博
      count += 1
  if hasNew :
    LogGet('\n\nhasNew is True:\n' + weibo + '\n' + url)
    #sendCloud.send(weibo[11:],url)
  if hasNew and '秒前' in weibo: # 满足刚刚更新的微博内容返回，不满足则添加进sended 文件
    return weibo,url
  else :
    return '',''

#weibos = getWeibo()
#如何确认是新消息:
#1 先提取网页上获取的微博内容、时间
#2 合成一条一条的微博，并判断是否在sendLst中（存在已推送微博的列表，
#  与sendLiu_date.log保持同步，sendLiu_date.log存放今日已推送， 还会包括之前推送
#  的部分微博)，不在则保存，若同时包含关键字‘秒前’，说明是新微博，需推送

#主程序run()思路逻辑：
#程序会在服务器每天指定的时间段运行，由runLiuWu.py 控制
#1、打开程序，读取文件sended_08.log，（08表示月份）初始化sendedLst，最多append10个，最少0个。
#2、每隔3s获取一次数据，分析是否有更新，有则发送，并更新sendedLst以及文件sended_08.log

def init() :
  lines = LogGetSended()
  length = len(lines)
  sendedLst = list()
  for i in range(length) :
    sendedLst.append(lines[i].strip('\n'))
  return sendedLst

def runOnce(sendedLst) :
  weibo,url = getNewWeibo(sendedLst)
  curtime = time.strftime('%H:%M:%S',time.localtime(time.time()))
  LogGet('get New ok!' + curtime)
  print '\n' + curtime
  print 'get New ok' + weibo
  if len(weibo) > 0 :
    LogGet('New weibo :' + weibo + '\n' + curtime)
    sendCloud.send(weibo[11:], url)
    #sendLiu.send( '刘鹏程SaiL微博更新', weibo) 
    #sendLiu.send( weibo[11:rpos] + '...', weibo) 
    LogGet('after send email')
  else :
    LogGet('None!\n' + curtime)

def run() :
  sendedLst = init()
  while True : #无限循环
    runOnce(sendedLst, date)
    time.sleep(3)

def test():
  lst = list()
  for i in range(1) :
    getNewWeibo(lst)
  #line 175
 # getWeibo()

#test()
