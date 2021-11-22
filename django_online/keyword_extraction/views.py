import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from keyword_extraction.textrank import wordRank, sentenceRank


def index(request):

    return render(request, 'index.html')


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

