# 文本自动摘要
BIT自然语言理解初步大作业2 
项目部署：www.0x404.tech


# 项目使用说明

## 直接在线访问本应用

* 本项目为web项目，项目已部署到云服务器，可通过网址http://www.0x404.tech 直接在线访问与使用本应用。
* 建议使用google游览器或者edge游览器
* 本文档为本地部署教程。

## 项目本地运行

### 下载项目


```shell
 #克隆github仓库到本地
 git clone git@github.com:0x404/BIT-NLP-P2.git
 
 #进入Django项目目录下
 cd BIT-NLP-P2/django_online/
```

### 需要的资源下载

由于使用的词向量表示和训练数据集过大，并没有作为提交文件的一部分提交，故如需在本地进行部署，请完成如下资源的下载：

+ 基于微博语料库训练的$300$维词向量
+ NLPCC2017摘要数据

#### 使用命令行命令自动下载（推荐）

使用脚本自动下载所需的数据文件，执行下列命令后无需手动下载资源，可以直接运行本项目。

```shell
#如果python没有wget库则先下载该库
pip install wget

#使用脚本下载语料库
python make.py
```

#### 手动下载

* 基于微博语料库训练的$300$维词向量300$维词向量，来源于https://github.com/Embedding/Chinese-Word-Vectors
  * 为加快下载，请从[此处](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/source/sgns.weibo.word.zip)下载。
* `NLPCC2017`摘要数据，来源于https://github.com/liucongg/GPT2-NewsTitle
  * 为加快下载，请从[此处](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/source/nlpcc_data.json)下载。

下载完成将如上资源放在目录`django_online/keyword_extraction/textrank/data`中即可

### 运行本Web应用

```shell
#运行程序
python manage.py runserver

#Starting development server at http://127.0.0.1:8000/
```

在浏览器地址栏输入`http://127.0.0.1:8000/`本地访问项目。

## 任务

- [x] textRank计算关键词
- [x] textRank计算关键句
- [x] web前端HTML界面
- [x] Django后端
- [ ] transformer

## 待做
- [x] 检查一个词在停用词表中 用字典树优化
- [x] 计算关键句中 用字典树优化
- [ ] 更细粒度的分句
- [x] textrank可以进一步改进，如加入句子长度的惩罚，或者使用句向量判断相似性


## 参考资料来源

* 停用词表来源：https://github.com/goto456/stopwords
* 清华数据集来源：http://thuctc.thunlp.org/
* 清华新闻数据集来源：https://thunlp.oss-cn-qingdao.aliyuncs.com/THUCNews.zip
* jieba(后续可以用作业1的库代替)
* re





