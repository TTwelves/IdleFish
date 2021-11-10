'''
# @Title:
# @Time : 2021/9/14 11:18
# @File : tools_config.py
# @Software: PyCharm

'''
import configparser

# 生成对象
cf = configparser.ConfigParser()

# 读取配置文件
filepath = r"C:\xjq\CodeRepo\IdleFish\config\config.ini"
cf.read(filepath, encoding="utf-8")

