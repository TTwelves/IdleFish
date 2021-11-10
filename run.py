'''
# @Title:
# @Time : 2021/9/14 12:07
# @File : run.py
# @Software: PyCharm

'''
from api import api_go
from libs.business.IdelFIshBusiness import IdelFishBusiness
from tools import tools_link, tools_CheckApp
from airtest.core.api import *
auto_setup(__file__)

class Main:

    def __init__(self):
        self.httpServer = '127.0.0.1:5037'
        self.deviceCode = 'EAF6GYMZNFLNHMSG'
        self.isInitedServer = False
        self.package = "com.taobao.idlefish"
        self.keyword = api_go.get_keyword()["keyword"]
        self.idle_fish = IdelFishBusiness(self.deviceCode, "红狗", self.httpServer)


    def run(self):
        while self.isInitedServer is False:
            tools_link.initServer(deviceCode=self.deviceCode, package=self.package, httpServer=self.httpServer)
            if tools_CheckApp.check() is False:
                continue
            else:
                self.isInitedServer =True

        self.idle_fish.run()


if __name__ == '__main__':
    main = Main()
    main.run()