'''
author: 0x404
Date: 2021-12-25 12:48:47
LastEditTime: 2021-12-25 12:56:59
Description: 
'''

import wget
from pathlib import Path

word2vec_path = "keyword_extraction/textrank/data/sgns.weibo.word"
testData_path = "keyword_extraction/textrank/data/nlpcc_data.json"

word2vec_url = "http://image-hosting-404.oss-cn-beijing.aliyuncs.com/source/sgns.weibo.word.bz2"
testData_url = "http://image-hosting-404.oss-cn-beijing.aliyuncs.com/source/nlpcc_data.json"

word2vec_file = Path(word2vec_path)
testData_file = Path(testData_path)


if word2vec_file.exists() == False:
    wget.download(word2vec_url, word2vec_path)

if testData_file.exists() == False:
    wget.download(testData_url, testData_path)