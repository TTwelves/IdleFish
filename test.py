# -*- encoding=utf8 -*-
__author__ = "1"

import re
from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/1f68f461?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH",])

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


class IdelFishBusiness:

    # 获取发货地
    def get_address(self):
        re2=poco("android.widget.ScrollView").children()
        for j in re2:
           name1 = j.get_name()
           cmp1 = re.search("发布于.*",name1)
           if cmp1 is not None:
               address = cmp1.group().replace("发布于", "")
               return address

    # 向下滑动至出现用户介绍：xxx来闲鱼xxx天了，卖出过xxx件宝贝
    def swipe_down(self):
        width, height = device().get_current_resolution()
        start_pt = (width, height)
        end_pt = (width, height / 2)
        swipe(start_pt, end_pt)

        # 终点判断
        re3=poco("android.widget.ScrollView").children()
        for j in re3:
           name1 = j.get_name()
           cmp1 = re.search("^.*\s*来闲鱼.*",name1)
           if cmp1 is not None:
            print(cmp1.group())

if __name__ == '__main__':

    keyword = "素力高"

    idlefish = IdelFishBusiness()

    #启动app
    start_app("com.taobao.idlefish")

    #点击进入搜索栏
    poco("com.taobao.idlefish:id/search_bg_img_front").click()

    # 点击搜索栏
    poco("android.widget.EditText").click()

    # 输入关键词
    text(keyword)

    # 点击搜索
    poco("搜索").click()

    # 最外层循环，遍历所有商品
    re1 = poco("android.widget.ScrollView").offspring()
    for i in re1:
        name1 = i.get_name()
        cmp1 = re.search(f".*{keyword}", name1)
        if cmp1 is not None:
            print(cmp1)
            print(name1)
            poco(name=name1).click()
            '''
            针对每一个用户进行数据抓取
            '''
            # 等待进入页面
            sleep(2)
            # 获取发货地址
            goods_address = idlefish.get_address()
            # 向下滑动至介绍栏
            idlefish.swipe_down()




#赞
print(poco("超赞").sibling()[0].get_name())
#关注
list1 =poco("超赞").parent().parent().child()[1].children().get_name()
for i in list1:
   print(i)
#粉丝数
print(poco("粉丝").sibling()[0].get_name())
# 实名认证
name_bool = poco(nameMatches="^芝麻信用.*").parent().parent().offspring("已认证").exists()

if name_bool is True:
   print("已认证")
else:
   print("未认证")









    