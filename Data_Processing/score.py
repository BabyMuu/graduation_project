""" @File   : score_point
    
    @Author : BabyMuu
    @Time   : 2023/2/4 12:16
"""
import random

import pymysql

from utils.driver import conn

examination_id = 2
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute(f"select * from user_scores where exam_id = {examination_id}")
students = cur.fetchall()
cur.execute(f'select * from user_questions where  exam_id = {examination_id}')
questions = cur.fetchall()
cur_scores = []
orders = []
rules = []

for stu in students:
    scores = stu.get('score').split(',')
    scores = list(map(int, scores))
    for i in range(len(scores)):
        if questions[i].get('types') <= 1:
            cur_scores.append('0' if scores[i] == 0 else '1')
        else:
            cur_scores.append('1' if scores[i] >= questions[i].get('score') * 0.6 else '0')
        if cur_scores[-1] == '1':
            orders.append(str(questions[i].get('exam_order')))
            rules.append(questions[i].get('name'))
    cur.execute(f"insert into user_scores (score, student_id, exam_id, score_situation)values ('{','.join(cur_scores)}',"
                f" {stu.get('id')}, "
                f"{examination_id}, '{','.join(orders)}', '{','.join(rules)}')")
    # cur.execute(f"insert into scores_order (score, student_id, examination_id)values ('{','.join(orders)}', {stu.get('id')}, "
    #             f"{examination_id})")
    # cur.execute(f"insert into scores_rule (score, student_id, examination_id)values ('{','.join(rules)}', {stu.get('id')}, "
    #             f"{examination_id})")
    orders = []
    cur_scores = []
    rules = []
