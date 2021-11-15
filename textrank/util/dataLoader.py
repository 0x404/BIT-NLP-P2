'''
author: 0x404
Date: 2021-11-15 13:07:42
LastEditTime: 2021-11-15 13:09:00
Description: 
'''


def loadStopWords(path):
    file = open(path, mode="r", encoding="utf-8")
    res = []
    for line in file:
        line = line.strip()
        line = line.strip('\n')
        res.append(line)
    return res