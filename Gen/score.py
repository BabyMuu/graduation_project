""" @File   : score
    
    @Author : BabyMuu
    @Time   : 2023/2/4 11:50
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
examination_id = 3
# 获取考试题目
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute(f"select * from user_questions where exam_id = {examination_id}")
questions = cur.fetchall()
scores = []
# 获取全部学生
cur = conn.cursor()
cur.execute("select user_id from user_students")
stus = cur.fetchall()

cur_scores = []
orders = []
rules = []
for examination_id  in range(1, 10):
    for sid in stus:
        sid = sid[0]
        score = 0
        for question in questions:
            que_score = question.get('score')
            types = question.get('que_type')
            if types <= 1:
                s = random.choice([0, que_score])
            else:
                s = random.choice(list(range(1, int(que_score) + 1)))
            scores.append(s)

        # cur.execute(f"insert into user_scores (score, student_id, examination_id)values ('{','.join(scores)}', {i}, 1)")
        for i in range(len(scores)):
            if questions[i].get('que_type') <= 1:
                cur_scores.append('0' if scores[i] == 0 else '1')
            else:
                cur_scores.append('1' if scores[i] >= questions[i].get('score') * 0.6 else '0')
            if cur_scores[-1] == '1':
                rules.append(questions[i].get('kno_point'))
        # cur.execute(f"insert into user_scores (score, student_id, exam_id, score_situation, score_know_situation)values ("
        #             f"'{','.join(cur_scores)}',{i},{examination_id}, '{','.join(cur_scores)}', '{','.join(list(set(rules)))}'"
        #             f" )")
        score_total = sum(scores)
        scores = list(map(str, scores))
        cur.execute(f"insert into user_scores (score, student_id, exam_id, score_situation, score_know_situation)values ("
                    f"'{score_total}',{sid},{examination_id}, '{','.join(scores)}', '{','.join(list(set(rules)))}'"
                    f" )")
        scores = []
        cur_scores = []
        rules = []
