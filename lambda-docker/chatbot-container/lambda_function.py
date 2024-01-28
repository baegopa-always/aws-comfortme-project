import json
import sys
from http import HTTPStatus
import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def predict(request):
    model_path='./korean_bert_model'
    model = SentenceTransformer(model_path)
    print("model imported")

    df_path='./df.pkl'
    df=pd.read_pickle(df_path)
    print("df read")
    
    embedding = model.encode(request)
    print("text encoded")
    df['similarity'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())

    answer = df.loc[df['similarity'].idxmax()]
    result=dict()
    result['division']=str(answer['구분'])
    result['response']=str(answer['챗봇'])
    result['simRequest']=str(answer['유저'])
    result['simRate']=float(answer['similarity'])

    print(f"response : {result['response']}   div:{result['division']}  simReq :{result['simRequest']}   simRate : {result['simRate']}")
    return result

def handler(event, context):
    try:
        data=json.loads(event['body'])
        request=data['request']
        print("request : ",request)
        response=predict(request)
        print("response 돌아옴")
        return {
            'statusCode':200,
            'body':json.dumps(response,ensure_ascii=False)}
    except Exception:
        logging.exception(Exception)
