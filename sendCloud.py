#coding=utf-8
import requests, json
import time
from log import LogEmail

mailUrl = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

apiFile = open('apiInfo.txt','r')
apiInfo = apiFile.readlines()
API_USER = apiInfo[0].strip()
API_KEY = apiInfo[1].strip()

def send(content,url) :
  LogEmail('\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) )
  LogEmail(content + '\n' + url)
  userFile = open('users_liu.txt','r')
  toLst = userFile.readlines()
  toNum = len(toLst)
  for i in range(toNum):
    toLst[i] = toLst[i].strip()
  
  weiboLst = list()
  urlLst = list()
  for i in range(toNum) :
    weiboLst.append(content)
    urlLst.append(url)

  sub_vars = {
    'to': toLst,
    'sub':{
      '%weibo%': weiboLst,
      '%url%': urlLst,
      }
    }

  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "template_invoke_name" : "template_liu",
    "substitution_vars" : json.dumps(sub_vars), 
    "from" : "liu@batch.wublogpush.com",
    "fromname" : "大刘推送",
    "subject" : "刘鹏程SaiL微博更新",
    "resp_email_id": "true",
    }
  
  r = requests.post(mailUrl, files={}, data=params)
  LogEmail(r.text)

#send('大刘微博内容','http://www.imaibo.net/space/1954702')

