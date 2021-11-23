'''
author: 0x404
Date: 2021-11-15 12:09:52
LastEditTime: 2021-11-15 16:07:03
Description: 
'''
import jieba
import math
from .util import dataLoader
from .util.trieTree import Trie

def generateMap(wordList):
    """
    对于一个分词结果，生成词到id的字典
    :param wordList: 分词后的词列表
    :return: word2Id, id2Word
    """
    word2Id, id2Word = {}, {}
    for word in wordList:
        if word not in word2Id.keys():
            value = len(word2Id)
            word2Id[word] = value
            id2Word[value] = word
    return word2Id, id2Word



def generateTrans(wordList, word2Id, windowLen = 3):
    """
    生成转移转移矩阵
    :param wordList: 句子分词后的词列表
    :param word2Id: 从词转向id的字典
    :param windowLen: 共现窗口大小，默认为3
    :return: 标准化的转移矩阵
    """
    n = len(word2Id)

    trans = [[0.0 for i in range(n)] for j in range(n)]

    for i in range(len(wordList)):
        for j in range(1, windowLen + 1):
            if i + j >= len(wordList):
                break
            id_x = word2Id[wordList[i]]
            id_y = word2Id[wordList[i + j]]
            trans[id_x][id_y] += 1.0
            trans[id_y][id_x] += 1.0    #权重设为转移次数而不是单纯的01

    for i in range(n):
        sumt = sum(trans[i])
        if sumt == 0:
            continue
        for j in range(n):
            trans[i][j] /= sumt
    
    return trans

def calculateRank(trans, iteration = 1000):
    """
    计算rank向量
    :param trans: 转移概率矩阵
    :param iteration: 迭代次数，默认1000次（收敛则立即返回）
    :return: rank向量
    """
    n = len(trans)
    d = 0.85
    rank = [ 1 / n for _ in range(n)]
    for ite in range(iteration):
        rank_n = [ 0.0 for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rank_n[i] += trans[j][i] * rank[j]
            rank_n[i] = 1 - d + d * rank_n[i]
        rank = rank_n
        
        norm = math.sqrt(sum( x * x for x in rank))
        norm_n = math.sqrt(sum(x * x for x in rank_n))
        if abs(norm - norm_n) < 0.01:   # 计算二范数 判断收敛
            break
    
    return rank
        

    

def wordRank(text, windowLen = 3, limit = 5):
    """
    给定一个句子，计算该句子中的前limit个关键词
    :param text: 待计算句子
    :param windowLen: 使用textrank算法的共现窗口大小，默认为3
    :param limit: 前limit个关键词，默认为5（但limit大于全部词时，返回全部词）
    :return: 前limit个关键词，以[(score, word1), (score, word2), (score, word3)...]的形式返回
    """
    stopWords = dataLoader.loadStopWords("/root/github/BIT-NLP-P2/django_online/keyword_extraction/textrank/data/baidu_stopwords.txt")  # 加载停用词
    trie = Trie(stopWords)

    segRes = [word for word in jieba.cut(text)]
    stopRes = []
    for word in segRes:
        if trie.isExist(word) == False:
            stopRes.append(word)    # 计算得到去除停用词的分词结果
    
    word2Id, id2Word = generateMap(stopRes) # 获得词与id的映射字典
    trans = generateTrans(stopRes, word2Id, windowLen) # 获得转移概率矩阵
    rank = calculateRank(trans) # 迭代计算

    for i in range(len(rank)):
        rank[i] = (rank[i], id2Word[i]) # 对id进行解码

    rank.sort(key=lambda s:(s[0]), reverse=True) # 按照score排序
    
    return rank[0 : min(len(rank), limit)]  # 返回前limit个结果
        
    
    
if __name__ == "__main__":
    text = '第十二届蓝桥杯大赛共吸引来自全国1200多所高校的6万多名学生参与，我校ACM俱乐部有48名学生从中脱颖而出，成功入围全国总决赛， 并在决赛中夺得全国一等奖3项，二等奖7项，三等奖16项。第十三届蓝桥杯全国软件和信息技术专业人才大赛报名现已正式开始，为鼓励更多具有编程兴趣的优秀学生参赛，ACM俱乐部现举办第十三届蓝桥杯校内选拔赛，具体内容如下：'
    res = wordRank(text=text, windowLen=5, limit=3)
    print (res)
    # res = [(0.20553703703703705, '全国'), (0.18641798941798943, '杯'), (0.18521428571428572, '蓝桥')]


