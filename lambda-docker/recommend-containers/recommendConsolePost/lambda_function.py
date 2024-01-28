import json
import sys
from http import HTTPStatus
import logging
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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

def  conductSqlQuery(sql,consolePostId):
    print("--------------------------------")
    print("conductSqlQuery function init")
    conn=getMysqlConn()
    curs = conn.cursor()
    with conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql,consolePostId)
                # result = json.dumps(cur.fetchall(),default=json_default,ensure_ascii = False)
                result = cur.fetchall()
    print("conductSqlQuery function done")
    print("--------------------------------")
    return result


def handler(event, context):
    try:
        print("--------------------------------")
        print("recommendConsolePost lambda_handler function init")
        params=event['queryStringParameters']
        consolePostId=params['consolePostId']
        print("consolePostId : ",consolePostId)
        
        sql = "SELECT * FROM ConsolePost WHERE consolePostId=%s"
        reqConsolePost=conductSqlQuery(sql,consolePostId)
        reqConsolePost=reqConsolePost[0]
        print("reqConsolePost : ", reqConsolePost)
        reqEmbedding=np.fromstring(reqConsolePost['bertEmbedding'].replace('[','').replace(']',''),sep=', ')
        print("reqEmbedding : ",reqEmbedding)
        
        sql = "SELECT * FROM ConsolePost WHERE consolePostId!=%s AND bertEmbedding IS NOT NULL "
        otherConsolePosts=conductSqlQuery(sql,consolePostId)
        df=pd.DataFrame(otherConsolePosts)
        df['bertEmbedding']=df['bertEmbedding'].apply(lambda x:np.fromstring(x.replace('[','').replace(']',''),sep=', '))
        print("dfOtherConsolePosts :", type(df))

        df['similarity'] = df['bertEmbedding'].map(lambda x: cosine_similarity([reqEmbedding], [x]).squeeze())
        df=df.sort_values(by=['similarity'],ascending=False)
        df=df.head(n=5)
        df=df.drop('bertEmbedding',axis=1)
        dfJson = df.to_json(orient = 'records')
        
        return  {
            'statusCode':200,
            'body':dfJson,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            }
        }
    except Exception:
        logging.exception(Exception)
        return False

