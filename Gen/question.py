""" @File   : main
    
    @Author : BabyMuu
    @Time   : 2023/2/4 11:32
"""
import random

import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    database='gra',
    charset='utf8',
    autocommit=True
)
cur = conn.cursor()
knowledge_points = ["有理数",
                    "三角形",
                    "三角函数",
                    "轴对称",
                    "不等式",
                    "二次根式",
                    "一元一次方程",
                    "一元二次方程",
                    "二元一次方程",
                    "实数",
                    "分式",
                    "整式",
                    "因式分解",
                    "一次函数",
                    "二次函数",
                    "反比例函数",
                    "平面直角坐标",
                    "四边形",
                    "圆",
                    "几何",
                    "概率"]
examination_id = 3
for e in range(1,10):
    for i in range(1, 16):
        types = 0
        score = 0
        knowledge_point = random.choice(knowledge_points)
        if i <= 5:
            types = 0
            score = 5
        elif i <= 10:
            types = 1
            score = 5
        else:
            types = 2
            score = 10
        cur.execute(f"insert into user_questions ( kno_point, que_type, exam_id, score, que_num) values ('{knowledge_point}', {types},"
                    f" {e},"
                    f" {score}, {i});")
