# -*- coding: utf-8 -*-

from igetui.igt_message import IGtAppMessage
from igetui.template.igt_notification_template import NotificationTemplate
from igt_push import IGeTui
import requests
import time
import json

APPID = 'xx4YtJHqfC6rezkYndlzD5'
APPKEY = 'xHyHtP3sjpAYuaf4YntShA'
MASTERSECRET = 'XYo36KsDWg9Ie9pPI6YRi7'
CID = 'e560b884d8d9bf5bc5a0f9da545a11f3'
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

#定义常量, appId、appKey、masterSecret 采用本文档 "第二步 获取访问凭证 "中获得的应用配置

push = IGeTui(HOST, APPKEY, MASTERSECRET)

# 新建一个推送模版, 以链接模板为例子，就是说在通知栏显示一条含图标、标题等的通知，用户点击可打开您指定的网页
template = NotificationTemplate()
template.appId = APPID
template.appKey = APPKEY
template.logo = ""
template.url = ""
template.transmissionType = 1
template.transmissionContent = ''
template.isRing = True
template.isVibrate = True
template.isClearable = True

#定义"AppMessage"类型消息对象，设置消息内容模板、发送的目标App列表、是否支持离线发送、以及离线消息有效期(单位毫秒)
message = IGtAppMessage()
message.isOffline = True
message.offlineExpireTime = 1000 * 600
message.appIdList.extend([APPID])

cnt = 1
while cnt <= 12:
    url = "http://www.nmc.cn/f/rest/real/54662?_=" + str(time.time())
    response = requests.get(url)
    parsed_json = json.loads(response.content)
    print parsed_json["weather"]["temperature"]
    template.title = u'报警'
    template.text = u'设备1 ' + str(parsed_json["weather"]["temperature"])
    message.data = template
    ret = push.pushMessageToApp(message)
    print ret
    time.sleep(300)
    cnt += 1
