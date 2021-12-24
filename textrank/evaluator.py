'''
author: 0x404
Date: 2021-12-24 10:33:50
LastEditTime: 2021-12-24 12:10:29
Description: 
'''

from rouge import Rouge
import sentenceRank
import jieba
import json



file = open("data/nlpcc_data.json", "rb")
data = json.load(file)

test_cases = 200
test_input = []
test_ans = []
pred_ans = []

for i in range(min(test_cases, len(data))):
    test_input.append(data[i]["content"])
    test_ans.append(data[i]["title"])

for i in range(len(test_input)):
    pred_y = sentenceRank.sentenceRank(test_input[i], limit=1)
    pred_ans.append(pred_y[0][1])
    print (i)


for i in range(len(test_ans)):
    test_ans[i] = ' '.join([word for word in jieba.cut(test_ans[i])])
    pred_ans[i] = ' '.join([word for word in jieba.cut(pred_ans[i])])

# print (pred_ans)
rouge = Rouge()
rouge_score = rouge.get_scores(pred_ans, test_ans)
print (rouge_score[0]["rouge-1"])