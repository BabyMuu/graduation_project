""" @File   : 2
    
    @Author : BabyMuu
    @Time   : 2023/5/1 13:54
"""
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
cur.execute("select user_id from user_students")
a = cur.fetchall()
for i in a:
    print(i[0])
