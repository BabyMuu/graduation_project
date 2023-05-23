""" @File   : kmeans
    
    @Author : BabyMuu
    @Time   : 2023/2/4 15:19
"""
import pymysql

from collections import defaultdict
import pandas as pd

from utils.driver import conn
from sklearn.cluster import KMeans
import warnings
import pymongo

# 忽略kmeans的警告
warnings.filterwarnings('ignore')

# 连接 mongodb 数据库
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["exam"]

examination_id = 2
# 获取连接, 游标
cur = conn.cursor(pymysql.cursors.DictCursor)

# 查询数据 -- 试题信息, 学生考试成绩信息
cur.execute(f"select * from scores where examination_id = {examination_id}")
students = cur.fetchall()
cur.execute(f'select * from question where  examination_id = {examination_id} order by exam_order')
questions = cur.fetchall()
# 获取当场考试每个知识点的总分
know_point_score = defaultdict(int)
for i in questions:
    know_point_score[i.get('name')] += i.get('score')

# 获取每个学生每个知识点的得分
stus = {}
for stu in students:
    stu_get_score = defaultdict(int)
    scores = stu['score'].split(',')
    for i in range(len(scores)):
        stu_get_score[questions[i].get('name')] += int(scores[i]) / know_point_score[questions[i].get('name')]
        stu_get_score[questions[i].get('name')] = round(stu_get_score[questions[i].get('name')], 2)
    stus[stu.get('id')] = stu_get_score
#
data = pd.DataFrame(stus)
# 对每个知识点得分情况聚类
ks = [KMeans(n_clusters=4, random_state=0) for i in range(len(data))]
for i in range(len(data)):
    ks[i].fit(data.iloc[i].values.reshape(-1, 1))
# 对得分情况进行分级
ls = []
for i in range(len(ks)):
    k = ks[i]
    kc = k.cluster_centers_
    y = k.labels_
    kc_list = sorted([i for i in kc[:, 0]])

    def my(x):
        if x == kc_list[0]:
            return "差"
        elif x == kc_list[1]:
            return "中"
        elif x == kc_list[2]:
            return "良"
        else:
            return "优"

    data.iloc[i] = [my(x) for x in kc[y]]
# 保存处理后的数据到MongoDB
ori_dic = data.to_dict()
dic_lst = [{
    'exam_id': examination_id,
    'name'   : str(i),
    'score'  : ori_dic[i]
}
    for i in ori_dic]
print(dic_lst)
# mycol.insert_many(dic_lst)
