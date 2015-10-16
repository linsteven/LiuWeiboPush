# LiuWeiboPush



###实现功能

实时邮件推送刘鹏程SaiL在投资脉搏上的[直播微博](http://www.imaibo.net/space/1954702)。
基本上10s内就可以收到邮件提醒。邮件内容是大刘的新微博内容。

###解决问题
使用投资脉搏客户端，关注的人发状态，不能实时提醒，设置了新消息提醒却无效。而这能实时提醒，不需经常刷新网页或客户端

###如何使用
代码是用python写的，版本2.7

1. 下载工程，请在release中下载__v1.0版本__
2. 修改sendLiu.py文件，将里面“linsgrabstock@163.com”全部替换为你的163邮箱（若没有，注册下，并开通SMTP，需绑定手机。开通后，会收到客户端授权码）;修改41行，替换自己邮箱以便接受程序运行相关通知
3. 新建文件pwd.txt，存放客户端授权码；
4. 新建log文件夹，存放日志；
5. users_liu.txt存放收件人邮箱
6. 运行run.py即可（没安装python的，[看这里缪雪峰的教程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001374738150500472fd5785c194ebea336061163a8a974000)）

###尝鲜体验
倘若你觉得上面的“如何使用”太复杂，又想体验这个邮件推送服务，鄙人愿意用自己的邮箱给大家免费发。你可以给我发邮件<linsgrabstock@163.com>，附上你的接收邮箱即可。


