""" @File   : draw
    
    @Author : BabyMuu
    @Time   : 2023/2/4 15:57
"""
import pymongo
import matplotlib.pyplot as plt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["exam"]
res = mycol.find_one({'exam_id': 2, 'name': '713'}, {'_id': 0, 'exam_id': 0, 'name': 0})
dic = res.get('score')
print(dic.keys(), dic.values())
