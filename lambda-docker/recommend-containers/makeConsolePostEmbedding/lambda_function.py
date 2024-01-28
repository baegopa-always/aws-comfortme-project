import json
import sys
from http import HTTPStatus
import logging
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pymysql


DB_HOST="db-team8-consolation.c8fut6pj2ay8.ap-northeast-2.rds.amazonaws.com"
DB_USER="root"
DB_PASSWORD="1tkddydwkdql"
DB_NAME="comfortmeDB"

def getMysqlConn():
    return pymysql.connect(
            host=DB_HOST, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            db=DB_NAME)


def addEmbToConsolePost(contents,consolePostId):
    model_path='./korean_bert_model'
    model = SentenceTransformer(model_path)
    print("model imported")

    npEmbedding = model.encode(contents)
    print("text encoded")
    npEmbeddingStr = str(npEmbedding.tolist())
    
    sql = "UPDATE ConsolePost SET bertEmbedding=%s WHERE consolePostId=%s"

    conn=getMysqlConn()
    curs = conn.cursor()
    curs.execute(sql, (npEmbeddingStr,consolePostId))
    conn.commit()
    conn.close()

def handler(event, context):
    try:
        print("event : ",event)
        data=json.loads(event['body'])
        contents=data['contents']
        consolePostId=data['consolePostId']
        print("contents : ",contents, "   consolePostId : ",consolePostId)

        addEmbToConsolePost(contents,consolePostId)
        return {
            'statusCode':200}
    except Exception:
        logging.exception(Exception)
        return False

