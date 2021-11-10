'''
# @Title:
# @Time : 2021/9/14 10:14
# @File : api_go.py
# @Software: PyCharm

'''
import json

import requests
from tools import tools_config

host = tools_config.cf.get('Api','host')

# 获取关键词
def get_keyword():
    path = "/getKeyword"
    data = {
        "splatform":"1"
    }
    return get_request(path,data)

# 上传数据,服务器返回判断,是否进行沟通
# 返回结果为：code=200 & can_reply = 1 可以发消息
'''
******************参数说明******************
| splatform：平台编号（闲鱼平台为：1）   
| address：发货地                      
| nick_name：用户昵称                  
| reg_date：注册日期                 
| sold_num：销量                    
| like_num：点赞数                   
| follow_num：关注数                 
| fans_num：粉丝数                   
| real_name：是否实名认证（1为是，0为否） 
| player：是否为闲鱼玩家（1为是，0为否） 
| uuid：用户ID 
| myuuid：本机账户ID
*********************************************
'''
def upload_data(address, nick_name, reg_date, sold_num, like_num, follow_num, fans_num, real_name, player, uuid, myuuid):
    path = "/saltedFish/isReplay"
    data ={
        "splatform": "1",
        "nick_name":nick_name,
        "address":address,
        "reg_date":reg_date,
        "sold_num":sold_num,
        "like_num":like_num,
        "follow_num":follow_num,
        "fans_num":fans_num,
        "real_name":real_name,
        "player":player,
        "uuid":uuid,
        "myuuid":myuuid
    }
    return get_request(path,data)

# get请求
def get_request(path,data):
    url = host + path
    response = requests.get(url=url,params=data)
    return response.json()

# post请求
def post_request(path,data):
    url = host + path
    response = requests.post(url=url,data=data)
    return response