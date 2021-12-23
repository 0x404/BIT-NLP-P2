# 自然语言理解初步大作业二

> 作者信息1：
>
> * 姓名：曾群鸿
> * 班级：07111905
> * 学号：1120192092
> * 联系电话：18959930736
> * 邮件地址：871206929@qq.com
>
> 作者信息2：
>
> * 姓名：舒敏宇
> * 班级：07111907
> * 学号：1120193028
> * 联系电话：15770550290
> * 邮件地址：3021019792@qq.com

**本项目为web项目，部署于http://www.0x404.tech，如无法访问请联系作者邮箱871206929@qq.com（或者QQ）**



## 核心思想与算法描述

文本摘要有两种实现方式，一种是基于生成的方式，通过使用RNN等神经网络进实现，另外一种是抽取的方式。

本次作业重点关注基于抽取式的文本自动摘要的实现，以及实现的算法——textrank。

pagerank算法应用于谷歌等搜索引擎中，通过网页链接的数量和质量来初略估计网页的重要性，从而对网页进行排名。textrank是基于pagerank算法的一种改进，它利用一篇文章内部词语共同出现的语义信息即可对一篇文章进行关键词抽取和关键句抽取，并且不需要依赖于语料库等训练数据。

下面从关键词抽取和关键句抽取两方面进行介绍。

### 关键词抽取

使用textrank进行关键词抽取的核心思想为利用词之间的相邻关系来构建一个词网络，然后使用pagerank的方式进行迭代计算，得到每个节点的权值，一个节点的权值越高其重要程度越高，故而得到关键词。

但可以发现，一个句子中有一些常用的词，如“的”、“了”等出现频率非常高，这类词也被称为停用词，尽管出现频率高但不可能作为关键词，所以一个句子总是将停用词去掉后再进行关键词的抽取。

具体算法描述如下：

1. 给定输入句子$input=w_1w_2w_3...w_n$

2. 使用jieba进行分词，得到输入句子的词序列$inputSeq=[w_1,w_2,...,w_n]$

3. 加载停用词表，对$inputSeq$中的词进行过滤，经过停用词表过滤后的词序列为$wordSeq=[w_1,w_2,...,w_k]$。

   由于在此步骤中主要操作可以描述为：查询一个给定词$w$是否在一个词典中，所以使用了字典树数据结构来进行优化，避免了一次查询需要扫描一次词典的低效操作。

4. 计算邻接矩阵$T_{i,j}$，其中$T_{i,j}=k$表示从词$i$转移到词$j$的次数为$k$，为了定义转移使用了一个共现窗口来定义，窗口的大小默认定义为$3$。那么如果$|i-j|\le 3$，则$w_i$可以转移到$w_j$且$w_j$也可以转移到$w_i$，也就是说$T$是一个对称矩阵。

   在完成转移次数的计算后，对$T$进行归一化计算$T_{i,j}=\frac{T_{i,j}}{\sum_{k=1}^{n}T_{i,k}}$，即$T_{i,j}$为从$w_i$到$w_j$转移的概率。

5. 通过如下公式对词网络进行迭代计算，直到收敛：
   $$
   val_i=(1-d)+d\times \sum_{j\in in(i)}\frac{W_{j,i}\times val_j}{\sum_{k\in out(j)W_{j,k}}}
   \\=(1-d)+d\times \sum_{j\in in(i)}T_{i,j}val_j
   $$
   为了判断收敛，我通过计算迭代前后两个$rank$相邻的二范数之差，如果两者之差小于$0.0001$则认为$rank$向量收敛

6. 根据$rank$向量，选择$rank$值最大的几个词当作本篇文章的关键词。

### 关键句抽取

基于textrank的关键句抽取核心思想与上述关键词抽取基本相同，在关键句抽取中以句子作为单位，而不是以此作为单位。

此时，邻接矩阵$T_{i,j}$不再是词$i$转移到词$j$的概率，而是句子$i$与句子$j$的相似性，关于句子$i$与句子$j$的相似度定义为：
$$
similarity_{i,j}=\frac{|\{w_k|w_k \in S_i \wedge w_k \in S_j\}|}{\log(|s_i|)\times \log(|s_j|)}
$$
这一相似度的定义虽然在某种程度上使两个句子之间建立了联系，但是没有考虑到词语与词语之间的词性相近等因素，如在句子$S_i$中有一个词"巨大"，而在$S_j$中有一个词"庞大"，由于这两个词不同所以对相似度没有正贡献。但是两个词的含义非常相近，应该考虑其对相似度的贡献，而不是由于词不同而简单省略。

因此，在此处对传统的textrank算法进行一个改进，转而使用word2vec词向量表示来计算句子的相似度，词向量能够考虑到词与词之间的距离，从而能更好地解决句子之间相似度的计算问题。

考虑使用一个$n$维的向量来表示词，那么定义一个句子$S=w_1w_2...w_k$的$n$维句向量：
$$
vec=\frac{1}{k}\sum_{i=1}^kvec_{w_i}
$$
式子中$vec_{w_i}$是$w_i$的词向量，即对句子中所有词的向量做一个简单的平均，得到句子的句向量。在得到句子的句向量后，句子的相似度定义为：
$$
similarity_{i,j}=\frac{\sum_{k=1}^nvec_{ik}\times vec_{jk}}{\sqrt(\sum^n_{k=1} vec_{ik}^2) \times \sqrt(\sum^n_{k=1} vec_{jk}^2) }
$$
即两个句子的相似度定义为两个句向量的点乘除于两个相邻二范数的乘积。

具体算法描述如下：

1. 给定输入文章$p=s_1s_2...s_n$
2. 使用正则表达式，将给定的文章分成句子列表$p=[s_1,s_2,...s_n]$
3. 对于每个句子$s_i$，对其进行分词和停用词过滤，得到$s_1=[w_1,w_2,...,w_n]$
4. 计算每个句子$s_i$的句向量$vec_i$
5. 计算转移矩阵$T_{i,j}=k$，其中$k$为上述定义的相似度
6. 使用同关键词抽取的迭代公式进行句子$rank$值的计算，直到收敛
7. 选择$rank$值最高的一个句子作为关键句

## 系统主要模块流程

系统架构如下图所示

![未命名文件(5)](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/未命名文件(5).png)

本系统基于django框架设计前后端web项目，可分为如下几个模块：

* 网页前端模块，前端模块中可分为向后端提交数据结构和从后端获取数据接口
* 后端响应模块，后端响应模块主要指django中的view函数模块，通过url指定view函数处理前端发送的请求事务
* 算法模块，完成关键词和关键句的抽取工作

三个模块的基本关系如下图所示：

![未命名文件(6)](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/未命名文件(6).png)

下面分别介绍各个模块的具体实现：
### 接口API设计

#### 界面访问

**简要描述：**

+ 用户访问主页面

**请求URL**

+ （根路径）`http://127.0.0.1:8000/`

**返回内容**

+ 主页面`index.html`

####  摘要及关键词获取

**简要描述：**

- 获取摘要以及关键词

**请求URL：**

- `http://127.0.0.1:8000/extract`

**请求方式：**

- POST

**参数：**

| 参数名        | 必选 | 类型   | 说明           |
| :------------ | :--- | :----- | -------------- |
| input_passage | 是   | string | 文章内容       |
| handle_method | 是   | string | 处理文章的算法 |

**返回示例**

```json
  {
    "status": True,
    "message": "",
    "keyword": "",
    "pdigest": ""
  }
```

**返回参数说明**

| 参数名  | 类型    | 说明                                      |
| :------ | :------ | ----------------------------------------- |
| status  | boolean | 状态信息；True：获取成功，False：获取失败 |
| message | string  | 详细错误信息                              |
| keyword | string  | 关键词内容                                |
| pdigest | string  | 摘要内容                                  |

### 网页前端模块

#### 导航栏部分

导航栏使用Flex弹性布局方式，导航栏内的元素进行两端对齐。左端元素为Logo，右端为用户相关内容。

#### 页面主体

##### 样式

页面的主体为左右布局，实现左右布局的方式为`Flex`弹性布局。页面之中的各个小组件，诸如按钮，单选框，标题，输入框均采用`bootstrap`内置的样式。另外，不允许用户复制*输入框以及输出框以外*的内容。

##### DOM节点控制以及网络请求

对`DOM`节点的控制使用JavaScript的经典库`JQuery`，当点击“提交”按钮的时候，通过JQuery获取*文章输入框*以及*处理算法选择框*的内容，获取内容之后，向后台发送`Ajax`请求，将文章内容以及处理方式发送到后台，获取后台的信息之后，对后台发送过来的内容进行分析，如果状态正常，则将*摘要*以及*关键词*现实在右边的对应方框之中。

```javascript
         $('#btnEditSave').click(function () {
            let postDate = {};
            $('#errorMag').text('');

            $('#input_area').find('input, textarea').each(function () {

                let v = $(this).val();
                let n = $(this).attr('name');
                if (n === 'handle_method'){
                    if ($(this).prop('checked')) {
                        postDate[n] = v;
                    }
                } else{
                    postDate[n] = v;
                }

            });

            console.log(postDate);

            $.ajax({
                url:'/extract/',
                type:'POST',
                data:postDate,
                success:function (arg) {
                    console.log(arg);
                    console.log(typeof(arg));
                    var dict = JSON.parse(arg);
                    if(dict.status){
                        console.log(dict);
                        $('#output_area').find('#keyword').val(dict.keyword);
                        $('#output_area').find('#pdigest').val(dict.pdigest);
                    }else{
                        $('#errorMag').text(dict.message);
                    }
                }
            })

        })
    })
```

点击“清空”按钮，将所有框之中的内容进行清除

```js
        //重置
        $('#clear_text').click(function () {
            $('#input_passage').val('');
            $('#pdigest').val('');
            $('#keyword').val('');
            $('#errorMag').text('');
            　$("input[type=radio][name='handle_method'][value='text_rank']").prop("checked",true);
        });
```


### 后端响应模块

因为使用前后端不分离的模式，通过Django的模板渲染显示前端页面，所以在`settings.py`修改以下内容

```python
#部署到服务器
ALLOWED_HOSTS = ['0x404.tech', 'www.0x404.tech',  'localhost', '127.0.0.1']

#添加模板渲染
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#静态资源访问
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

对访问的URL进行正则表达式方式的匹配，并与对应的Controller进行对应。

在`urls.py`之中添加显示以下内容

```python
urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('^$', views.index),
    re_path('^extract/', views.extract)
]
```

在`views.py`之中对前端的请求进行处理

+ 主页面渲染

  ```python
  def index(request):
      return render(request, 'index.html')
  ```

+ 关键词摘要请处理
  返回给前端页面`json`格式的数据，message表示错误信息，当处理失败的时候，前端通过后端传来的`status`以及`message`两个关键词进行相应的错误处理。

  ```python
  def extract(request):
      respone = {'status': True, 'message': None, 'keyword': None, 'pdigest': None}
  
      try:
          input_psg = request.POST.get('input_passage')
          handle_method = request.POST.get('handle_method')
  
          word3 = wordRank.wordRank(input_psg, limit = 3)
          digest = sentenceRank.sentenceRank(input_psg, limit = 1)
  
          keyword, pdigest = "", ""
          for w in word3:
              keyword += w[1] + " "
          keyword = keyword[0 : len(keyword) - 1]
          for w in digest:
              pdigest += w[1] + " "
  
          respone['keyword'] = keyword
          respone['pdigest'] = pdigest
  
  
      except Exception as e:
          print(e)
          respone['status'] = False
          respone['message'] = '获取结果失败'
  
      result = json.dumps(respone, ensure_ascii=False)
      return HttpResponse(result)
  ```


### 算法模块

算法模块涉及到的内容以及在“核心思想与算法描述”中介绍，将实现textrank所需要的各种数据集，数据结构和代码封装成一个包，并向外提供两个接口：

* sentenceRank：摘要抽取接口，输入文章，输出指定个数摘要
* wordRank：关键词抽取接口，输入文章，输出指定个数的关键词

将该算法工具包嵌入到django的框架中，通过后端响应模块的view函数进行调用，实现模块之间数据的传递

## 实验结果及分析



## 分工情况
