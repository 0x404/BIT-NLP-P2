# -*- coding:utf-8 -*-
'''
author: 0x404
Date: 2021-11-15 14:07:42
LastEditTime: 2021-12-24 11:02:49
Description: 
'''
import re
import jieba
import pickle
import math
import numpy as np
from util import dataLoader
from util.trieTree import Trie

def generateMap(sentList):
    """
    对于一个分句结果，生成句子到id的字典
    :param wordList: 分句后的句列表
    :return: sent2Id, id2Sent
    """
    sent2Id, id2Sent = {}, {}
    for sent in sentList:
        value = len(sent2Id)
        sent2Id[sent] = value
        id2Sent[value] = sent
    return sent2Id, id2Sent

def sentWord2vec(sent, vecMap):
    """
    对于一个句子，生成其句向量表示
    :param sent: 句子的分词结果
    :param vecMap: 词向量词典
    :return: 一个300维的句向量表示
    """
    vec = [0.0 for i in range(300)]
    if len(sent) == 0:
        return vec

    for word in sent:
        wordVec = [0.0 for i in range(300)]
        if word in vecMap.keys():
            wordVec = vecMap[word]
        for i in range(300):
            vec[i] += wordVec[i]
    for i in range(300):
        vec[i] /= len(sent)
    return vec
        

def similarity(sent1, sent2, vecMap):
    """
    计算两个分词后句子的相似度
    :param sent1: 句子1
    :param sent2: 句子2
    :param vecMap: 词向量词典
    :return: 两个句子的相似度
    """
    if len(sent1) == 0 or len(sent2) == 0:
        return 0.0
    sent1 = sentWord2vec(sent1, vecMap)
    sent2 = sentWord2vec(sent2, vecMap)

    vec1 = np.array(sent1)
    vec2 = np.array(sent2)
    f = np.sum(vec1 * vec2)
    p = np.sqrt(sum(vec1 ** 2))
    r = np.sqrt(sum(vec2 ** 2))
    return f / (p * r)
    # sent1 = 
    

def generateTrans(sentList, sent2Id, vecMap):
    """
    生成转移转移矩阵
    :param wordList: 句子分词后的词列表
    :param word2Id: 从词转向id的字典
    :param vecMap: 词向量词典
    :return: 标准化的转移矩阵
    """

    n = len(sent2Id)

    trans = [[0.0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            value = similarity(sentList[i], sentList[j], vecMap)
            trans[i][j] = trans[j][i] = value

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
    if n == 0:
        return []
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
        

def sentenceRank(paragraph, limit = 3):
    """
    给定一篇文章，计算该文章中的前limit个句子
    :param text: 待计算文章
    :param limit: 前limit个句子，默认为3（但limit大于全部句子个数时，返回全部句子）
    :return: 前limit个句子，以[(score, sent1), (score, sent2), (score, sent3)...]的形式返回
    """
    sentences = re.split(r'。|！|\!|\.|？|\?', paragraph)
    sent2Id, id2Sent = generateMap(sentences)

    for i in range(len(sentences)):
        sentences[i] = [word for word in jieba.cut(sentences[i])]
    stopWords = dataLoader.loadStopWords("./data/cn_stopwords.txt")  # 加载停用词
    trie = Trie(stopWords)
    newSent = []
    for i in range(len(sentences)):
        sent = []
        for w in sentences[i]:
            if trie.isExist(w) == False:
                sent.append(w)
        newSent.append(sent)
    
    wordSet = []
    for sent in newSent:
        for word in sent:
            if word not in wordSet:
                wordSet.append(word)
    
    vecMap = dataLoader.loadWord2vec("data/sgns.weibo.word", wordSet)
    
    trans = generateTrans(newSent, sent2Id, vecMap)
    rank = calculateRank(trans)

    for i in range(len(rank)):
        rank[i] = (rank[i], id2Sent[i])
    
    rank.sort(key=lambda s:(s[0]), reverse=True)

    return rank[0 : min(len(rank), limit)]
        
    
    
if __name__ == "__main__":
    paragraph = '党的历史是最生动、最有说服力的教科书，我们党历来高度注重总结历史经验。党一步步走过来，很重要的一条就是不断总结经验、提高本领，不断提高应对风险、迎接挑战、化险为夷的能力水平。一百年来，党领导人民进行伟大奋斗，在进取中突破，于挫折中奋起，从总结中提高，积累了宝贵的历史经验。党的十九届六中全会审议通过的《中共中央关于党的百年奋斗重大成就和历史经验的决议》概括了具有根本性和长远指导意义的十条历史经验：坚持党的领导，坚持人民至上，坚持理论创新，坚持独立自主，坚持中国道路，坚持胸怀天下，坚持开拓创新，坚持敢于斗争，坚持统一战线，坚持自我革命。这十条历史经验是系统完整、相互贯通的有机整体，深刻揭示了党和人民事业不断成功的根本保证，深刻揭示了党始终立于不败之地的力量源泉，深刻揭示了党始终掌握历史主动的根本原因，深刻揭示了党永葆先进性和纯洁性、始终走在时代前列的根本途径，具有重大的历史意义和现实指导意义。'
    print (sentenceRank(paragraph, limit=1))
    # print (len(res))
    # file = open("data/vecMap.pkl", mode="rb")
    # res = pickle.load(file)
    # file.close()
    # print (len(res))
    #[(0.3197129256305196, '这十条历史经验是系统完整、相互贯通的有机整体，深刻揭示了党和人民事业不断成功的根本保证，深刻揭示了党始 终立于不败之地的力量源泉，深刻揭示了党始终掌握历史主动的根本原因，深刻揭示了党永葆先进性和纯洁性、始终走在时代前列的根本途径，具有重大的历史意义和现实指导意义'), 
    # (0.31356540961997004, '党的历史是最生动、最有说服力的教科书，我们党历来高度注重总结历史经 验'), 
    # (0.30285869560446377, '一百年来，党领导人民进行伟大奋斗，在进取中突破，于挫折中奋起，从总结中提高，积累了宝贵的历史经验')]


