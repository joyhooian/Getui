# -*- coding: utf-8 -*-

from Getui import Test
import requests
import time
import json

cnt = 1
while cnt <= 12:
    url = "http://www.nmc.cn/f/rest/real/54662?_=" + str(time.time())
    response = requests.get(url)
    parsed_json = json.loads(response.content)
    print parsed_json["weather"]["temperature"]
    test = Test()
    test.pushMessageToApp(u'报警', u'设备1 ' + str(parsed_json["weather"]["temperature"]))
    test.pushMessageToApp(u'报警', u'设备2 ' + str(parsed_json["weather"]["temperature"]))
    time.sleep(300)
    cnt += 1