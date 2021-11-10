# import argparse
#
# # 解析命令行传入参数
# parser = argparse.ArgumentParser(description='manual to this script')
# parser.add_argument('--deviceCode', type=str, default=None)
# parser.add_argument('--env', type=str, default="local")
# parser.add_argument('--platform', type=str, default="tieba")
# args = parser.parse_args()
#
#
# print(args.deviceCode)
from datetime import date, timedelta

import requests
from airtest.core.android.adb import ADB
from airtest.core.api import connect_device

devices = []
adb = ADB()
deviceList = adb.devices()
for item in deviceList:
    devices.append(item[0])
print(devices)
# url = "http://116.62.78.32:8881/saltedFish/isReplay?splatform=1&address=成都&nick_name=守护猫咪老师呀&reg_date=2016-03-19&sold_num=291&like_num=29&follow_num=0&fans_num=19&real_name=1&player=0&uuid=xj1258236365&myuuid=夜雨声烦49103275"
# response = requests.post(url)
#
# print(response.text)
#
# list1= [1,2]
#
# if 1 in list1 and 2 in list1:
#     print("yes")


# httpServer = '127.0.0.1:5037'
# deviceCode = 'IBWGGMBYQSQKJB9H'
# connect_device("android://" + httpServer + "/" + deviceCode + "?cap_method=javacap&touch_method=adb")

