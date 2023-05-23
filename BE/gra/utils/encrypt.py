""" @File   : encrypt
    
    @Author : BabyMuu
    @Time   : 2023/2/9 15:09
"""
import hashlib

def encryption(plaintext):
    m = hashlib.md5()
    m.update("heighten".encode())  # 加盐 1
    m.update(plaintext.encode())  # 实际密码
    m.update("yous".encode())  # 加盐 2
    return m.hexdigest()
