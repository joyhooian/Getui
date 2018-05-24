# -*- coding: utf-8 -*-
import socket
import threading
import sys
import os
import struct

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

def checkAndPush():
    f = open("config.txt", 'rb')
    test = int(f.readline())
    f.close()
    url = "http://www.nmc.cn/f/rest/real/54662?_=" + str(time.time())
    response = requests.get(url)
    parsed_json = json.loads(response.content)
    print parsed_json["weather"]["temperature"]
    if test <= int(parsed_json["weather"]["temperature"]):
        template.title = u'报警'
        template.text = u'设备1 ' + str(parsed_json["weather"]["temperature"])
        message.data = template
        ret = push.pushMessageToApp(message)
        print ret

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #s.bind(('127.0.0.1', 51423))
        s.bind(('198.13.44.67', 51423))
        s.listen(1)
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'


    while 1:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            print "here"
            check = threading.Timer(300, checkAndPush)
            check.start()
        else:
            t = threading.Thread(target=deal_data, args=(conn, addr))
            t.start()


def deal_data(conn, addr):
    print 'Accept new connection from {0}'.format(addr)
    #conn.settimeout(500)
    conn.send('Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = "config.txt"
            #fn = filename.strip('\00')
            new_filename = os.path.join('./', fn)
            print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                 filesize)

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print 'start receiving...'

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print 'end receive...'
        conn.close()
        break

socket_service()
#if __name__ == '__main__':
#    socket_service()
