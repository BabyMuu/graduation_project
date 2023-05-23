""" @File   : score_rate
    
    @Author : BabyMuu
    @Time   : 2023/2/4 13:37
"""

import random

import pymysql

from utils.driver import conn

examination_id = 2

cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute(f"select * from scores where examination_id = {examination_id}")
students = cur.fetchall()
cur.execute(f'select * from question where  examination_id = {examination_id}')
questions = cur.fetchall()

for i in rang