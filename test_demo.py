import datetime
# import yaml
#
# map1={"jacky":[{"age":13},{"sex":"man"}]}
# list2=["jackyy",1,2,3,4]
# with open("./test.yaml","r",encoding="UTF-8") as f:
#     datas = yaml.safe_load(f)
#
# print(type(datas),datas)
# for k in datas:
#     print(k)
#     print(datas[k])
#


dt = datetime.date.today()

regist_time = dt + datetime.timedelta(days=-1000)

print(regist_time)
