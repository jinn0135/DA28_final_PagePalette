import requests
import re
import json

def summarize_text(text):
    url = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'
    client_id = '7ie1n9fatv'
    client_secret = 'ALFMzAMwzrzHuVUr1kA7gT3NdcffWgu0Dq2L2H1o'

    # 텍스트를 2000 단어로 제한
    text = text[:2000]

    request_body = {
        "document": {
            "content": text
        },
        "option": {
            "language": 'ko',
            "model": "news",
            "summaryCount": 2,
            "tone": 0
        }
    }
    headers = {
        'Accept': 'application/json;UTF-8',
        'Content-Type': 'application/json;UTF-8',
        'X-NCP-APIGW-API-KEY-ID': client_id,
        'X-NCP-APIGW-API-KEY': client_secret
    }

    response = requests.post(url, headers=headers, data=json.dumps(request_body).encode('UTF-8'))
    rescode = response.status_code

    if rescode == 200:
        summary = response.text
    else:
        print("Error : " + response.text)
        summary = ""
    article = re.sub(r'\\|\'|\n|n|\"', '', summary).split(':')[1].rstrip('}')
    return article