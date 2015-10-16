#coding: utf-8
import smtplib
import base64
import time
import random
import re

from email.mime.text import MIMEText
from email.header import Header


def send(strSubject, content, opt = '') :
  smtpserver = 'smtp.163.com'
  username = 'linsgrabstock@163.com'
  pwdFile = open('pwd.txt', 'r')
  password = pwdFile.readline().strip()
  pwdFile.close()
  username = base64.encodestring(username).strip() 
  password = base64.encodestring(password).strip() 
  date = time.strftime('%Y%m%d', time.localtime(time.time()))
  userFile = open('users_liu.txt','r')
  emails = userFile.readlines()
  logFile = open('./log/sendemail_' + date +'.log','a') #write only ,append
  logFile.write('\n\n-----------------\nLiu Send Content: \n' + content + '\n')
  mesg = '\n\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())
  smtp = smtplib.SMTP()
  try :
    smtp.connect("smtp.163.com: 25")
    mesg += '\n' + str(smtp.docmd('helo', username) ) 
    mesg += '\n' + str(smtp.docmd('auth login'))
    mesg += '\n' + str(smtp.docmd(username))
    mesg += '\n' + str(smtp.docmd(password))
    strFrom = '<linsgrabstock@163.com>'
    mesg += '\n' + str(smtp.docmd('mail from:', strFrom))
    if len(opt) == 0:
      for usermail in emails :
        usermail = usermail.strip()
        usermail = '<' + usermail + '>'
        mesg += '\n' + str(smtp.docmd('rcpt to:', usermail))
        mesg += '\n' + 'send to ' + usermail 
    else :  #inform myself 
      usermail = '<youremail@qq.com>' #改成自己的邮箱
      mesg += '\n' + str(smtp.docmd('rcpt to:', usermail))
      mesg += '\n' + 'send to ' + usermail

    mesg += '\n' + str(smtp.docmd('data'))
    mesg += '\n' + str(smtp.docmd('from: linsgrabstock@163.com\r\n' + 
    'to: receiver@qq.com\r\n' + 
    'subject: ' + strSubject + '\r\n\r\n' + 
    content + '\r\n' + 
    '.'))
    smtp.quit()
    logFile.write(mesg)
    logFile.close()
    return True
  except Exception, e:
    mesg += 'exception :' + str(e)
    logFile.write(mesg)
    logFile.close()
    return False

def informMyself(mesg) :
  send(mesg + 'aliyun', mesg, 'send to me')

def test() : #testAmount
  count = 0
  if True :
   send('测试邮箱容量' + str(count), 'this is a simple test. No.' + str(count), 'hello')
   count += 1

#test()

