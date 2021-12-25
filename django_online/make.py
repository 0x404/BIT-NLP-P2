'''
author: 0x404
Date: 2021-12-25 12:48:47
LastEditTime: 2021-12-25 13:24:45
Description: 
'''

import wget
import zipfile
from pathlib import Path


def unzip(file_path, file_name):
    zip_file = zipfile.ZipFile(file_path)
    for file in zip_file.namelist():
        zip_file.extract(file, file_name)

word2vec_path = "keyword_extraction/textrank/data/sgns.weibo.word"
testData_path = "keyword_extraction/textrank/data/nlpcc_data.json"

word2vec_url = "http://image-hosting-404.oss-cn-beijing.aliyuncs.com/source/sgns.weibo.word.zip"
testData_url = "http://image-hosting-404.oss-cn-beijing.aliyuncs.com/source/nlpcc_data.json"

word2vec_file = Path(word2vec_path)
word2vec_zip_file = Path(word2vec_path + ".zip")
testData_file = Path(testData_path)

print ("checking file ...")
if word2vec_file.exists() == False and word2vec_zip_file.exists() == False:
    print ("downloading file sgns.weibo.word.zip ...")
    wget.download(word2vec_url, word2vec_path + ".zip")
    print ("download finished!")
    print ("extracting file ...")
    unzip(word2vec_path + ".zip", "keyword_extraction/textrank/data")
    print ("extracting finished!")

if testData_file.exists() == False:
    print ("downloading nlpcc_data.json ...")
    wget.download(testData_url, testData_path)
    print ("download finished!")

print ("finished!")