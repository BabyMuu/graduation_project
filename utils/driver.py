""" @File   : driver
    
    @Author : BabyMuu
    @Time   : 2023/2/4 13:06
"""
import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    database='graduation',
    charset='utf8',
    autocommit=True
)
