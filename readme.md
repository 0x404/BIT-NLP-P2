# 文本自动摘要
BIT自然语言理解初步大作业2 

## 文件结构

* textrank

  * cn_stopwords.txt	#停用词表
  * wordRank    # 利用textrank算法计算关键词
  * sentenceRank    # 利用textrank算法计算关键句
  * dataLoader    # 加载数据
  

  

## 任务

- [x] textRank计算关键词
- [x] textRank计算关键句
- [ ] web前端HTML界面
- [ ] Django后端
- [ ] transformer

## 待做
- [ ] 检查一个词在停用词表中 用字典树优化
- [ ] 计算关键句中 用字典树优化
- [ ] 更细粒度的分句
- [ ] textrank可以进一步改进，如加入句子长度的惩罚，或者使用句向量判断相似性


## 参考资料来源

* 停用词表来源：https://github.com/goto456/stopwords
* 清华数据集来源：http://thuctc.thunlp.org/
* 清华新闻数据集来源：https://thunlp.oss-cn-qingdao.aliyuncs.com/THUCNews.zip
* jieba(后续可以用作业1的库代替)
* re



