# -*- encoding=utf8 -*-
__author__ = "许家麒"

import re
from datetime import date, timedelta

import yaml
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.exceptions import PocoNoSuchNodeException
from poco.utils import hrpc
from urllib3.exceptions import NewConnectionError


class IdelFishBusiness:

    # 获取发货地
    def get_address(self):
        info =[]
        re2 = poco("android.widget.ScrollView").children()
        for j in re2:
            name1 = j.get_name()
            cmp1 = re.search(".*[\s]*.*发布于.*", name1)
            if cmp1 is not None:
                temporary_data = cmp1.group()

                name1 = re.search(".*\s", temporary_data)
                name2 = name1.group().strip()
                print("昵称是：", name2)
                info.append(name2)

                address1 = re.search("发布于.*", temporary_data)
                address2 = address1.group().replace("发布于", "")
                print("地址是：", address2)
                info.append(address2)

                return info

    # 向下滑动至出现用户介绍：xxx来闲鱼xxx天了，卖出过xxx件宝贝
    def swipe_down_get_date_salenums(self, username):
        cmp1 = None
        while cmp1 is None:
            re3 = poco("android.widget.ScrollView").children()
            for j in re3:
                name1 = j.get_name()
                cmp1 = re.search("^全部留言.*", name1)
                if cmp1 is not None:
                    break
            poco("android.widget.ScrollView").swipe('up')

        info = []
        re4 = poco("android.widget.ScrollView").children()
        for k in re4:
            name2 = k.get_name()
            cmp2 = re.search(f"^{username}\s*.*", name2)
            if cmp2 is not None:

                temp = cmp2.group()

                try:
                    date1 = re.search("来闲鱼\d*天了", temp)
                    date2 = re.search("\d{1,10}", date1.group())
                except AttributeError:
                    print("日期：")
                    info.append(" ")
                else:
                    regist_date = self.transfor_datetime(int(date2.group()))
                    print("日期：", regist_date)
                    info.append(regist_date)

                try:
                    sale_nums1 = re.search("卖出过\d*件宝贝", temp)
                    sale_nums2 = re.search("\d{1,10}", sale_nums1.group())
                except AttributeError:
                    print("销量：")
                    info.append(" ")
                else:
                    print("销量", sale_nums2.group())
                    info.append(sale_nums2.group())

        return info

    # 继续下滑,点击个人介绍，进入个人主页
    def goto_person_page(self, username):
        re4 = poco("android.widget.ScrollView").children()
        for k in re4:
            name1 = k.get_name()
            cmp1 = re.search(f"^{username}\s*.*", name1)
            if cmp1 is not None:
                poco(name=name1).click()
                break

    # 获取点赞数、粉丝数、关注数、实名认证与否
    def get_account_data(self):
        info = []
        # 赞
        like_nums = poco("超赞").sibling()[0].get_name()
        print("点赞：",like_nums)
        info.append(like_nums)

        # 关注
        concern_nums = poco("超赞").parent().parent().child()[1].child().get_name()
        print("关注：",concern_nums)
        info.append(concern_nums)

        # 粉丝数
        fans_nums = poco("粉丝").sibling()[0].get_name()
        print("粉丝：",fans_nums)
        info.append(fans_nums)

        # 实名认证
        name_bool = poco(nameMatches="^芝麻信用.*").parent().parent().offspring("已认证").exists()

        if name_bool is True:
            print("已认证")
            info.append(True)
        else:
            print("未认证")
            info.append(False)

        return info

    # 获取账户ID
    def get_account_id(self):

        if poco("详情").exists() is True:
            poco("详情").click()

        account_id = poco("com.taobao.idlefish:id/weex_render_view").offspring("android.widget.LinearLayout").child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout")[
                  1].child("android.widget.FrameLayout")[2].child("android.widget.FrameLayout")[1].child(
            "android.widget.FrameLayout")[0].offspring("android.widget.ImageView").parent().child()[1].get_name()

        return account_id

    # 判断是否为"闲鱼玩家"
    def is_idlefish_vip(self, username):
        sign = poco(username).parent().child()[1].get_name()
        if sign == "宠物玩家":
            return True
        else:
            return False

    # 个人主页返回至商品页面
    def back_to_01(self):
        poco("com.taobao.idlefish:id/weex_render_view").child("android.widget.FrameLayout").child(
            "android.widget.FrameLayout")[0].child("android.widget.FrameLayout").child("android.widget.FrameLayout")[
            0].child("android.widget.FrameLayout").child("android.widget.FrameLayout").child(
            "android.widget.FrameLayout")[0].child("android.widget.ImageView").click()

    #对话框返回商品页面
    def back_to_02(self):
        poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child(
            "android.view.View").child("android.view.View").child("android.view.View").offspring("返回").child(
            "图片").click()

    # 商品页返回主页
    def back_to_main(self):
        poco("返回").click()

    # 进入对话框
    def go_to_chat(self):
        poco("我想要").click()
        # todo:发送文字+图片

    # 数据存入操作
    def dump_to_yaml(self,datalist:list):
        data_key = datalist[0]
        del datalist[0]
        data_dict = {data_key:datalist}
        with open("./test.yaml","a",encoding="utf-8") as f:
            yaml.dump(data_dict,f)

    # 数据读取操作
    def load_to_yaml(self)->list:
        with open("./test.yaml","r",encoding="utf-8") as f:
            datas = yaml.safe_load(f)
        # 用于存入所有已记录的用户名
        UserNameList = []
        for i in datas:
            UserNameList.append(i)

        return UserNameList

    # 换算出注册日期
    def transfor_datetime(self, days:int):
        today_date = date.today()
        regist_date = today_date + timedelta(days=-days)
        return regist_date

    # 获取目前登录账号的ID
    def get_my_id(self):

        new_msg = ""

        poco("android:id/content").offspring("我的，未选中状态").offspring("com.taobao.idlefish:id/tab_icon").click()

        re5 = poco("设置").parent().children()

        for i in re5:
            msg = re.search("会员名：.*", i.get_name())
            if msg is not None:
                new_msg = msg.group().replace("会员名：", "")

        poco("android:id/content").offspring("闲鱼，未选中状态").offspring("com.taobao.idlefish:id/tab_icon").click()

        return new_msg

if __name__ == '__main__':

    '''
    针对每一个用户进行数据抓取
    UserInfo = [0 昵称,1 发货地,2 注册日期,3 销量,4 点赞,5 关注,6 粉丝数,7 是否实名认证, 8 是否为闲鱼玩家，9 目标用户的ID , 10 当前登录账户的ID]
    '''

    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=[
            "android://127.0.0.1:5037/1f68f461?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH", ])

    from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)



    UserInfo =[]

    keyword = "冠能"

    idlefish = IdelFishBusiness()

    # 获取已记录的用户名
    UserNameList = idlefish.load_to_yaml()

    # 启动app
    start_app("com.taobao.idlefish")
    sleep(5)

    my_uid = idlefish.get_my_id()
    sleep(5)

    # 点击进入搜索栏
    poco("com.taobao.idlefish:id/search_bg_img_front").click()

    # 点击搜索栏
    poco("android.widget.EditText").click()

    sleep(2)

    # 输入关键词
    text(keyword,False)

    sleep(2)

    # 点击搜索
    poco("搜索").click()

    sleep(5)

    # 最外层循环，遍历所有商品
    re1 = poco("android.widget.ScrollView").offspring()
    for i in re1:
        name1 = i.get_name()
        cmp1 = re.search(f".*{keyword}", name1)
        if cmp1 is not None:
            poco(name=name1).click()
            # 等待进入页面
            sleep(2)

            # 获取昵称、发货地址
            try:
                Username_address = idlefish.get_address()
                UserInfo += Username_address
            except PocoNoSuchNodeException:
                keyevent("back")
                sleep(5)
                continue

            username = UserInfo[0]

            # 判断是否重复获取，如果是已获取过信息的用户，则跳过
            if username in UserNameList:
                keyevent("back")
                UserInfo = []
                # 返回主页后下滑
                poco.scroll(direction="vertical", percent=0.3, duration=1.0)
                sleep(5)
                continue

            # 向下滑动至介绍栏
            # 返回时间和销量
            date_saleNumbers = idlefish.swipe_down_get_date_salenums(username)
            UserInfo += date_saleNumbers

            # 继续下滑,点击个人介绍，进入个人主页
            idlefish.goto_person_page(username)

            sleep(5)

            # 获取点赞数、关注数、粉丝数、实名认证与否
            account_datas = idlefish.get_account_data()
            UserInfo += account_datas

            # 判断是否为闲鱼玩家
            idlefish_vip = idlefish.is_idlefish_vip(username)
            UserInfo.append(idlefish_vip)

            # 获取账号ID
            account_id = idlefish.get_account_id()
            UserInfo.append(account_id)

            # 返回上一页
            idlefish.back_to_01()
            sleep(2)

            '''
            判断是否符合条件进入对话，点击对话框
            若账号为 闲鱼玩家 则直接进入对话
            
            条件1：已经沟通过的用户，无需再次沟通，验证重复UserName
            条件2：销量 >= 40
            条件3：粉丝数 >= 100
            条件4：实名认证：是
            '''
            if UserInfo[8] is True:
                idlefish.go_to_chat()
                sleep(5)
                idlefish.back_to_02()
            else:
                if int(UserInfo[3]) >= 40:
                    if int(UserInfo[6]) >= 100:
                        if UserInfo[7] is True:
                            idlefish.go_to_chat()
                            sleep(5)
                            idlefish.back_to_02()

            sleep(2)

            UserInfo.append(my_uid)
            print(UserInfo)

            # 存入数据至yaml
            idlefish.dump_to_yaml(UserInfo)

            # 清空数组
            UserInfo = []

            idlefish.back_to_main()
            # 每读取一次数据，向下滑动一次
            poco.scroll(direction="vertical", percent=0.3, duration=1.0)











