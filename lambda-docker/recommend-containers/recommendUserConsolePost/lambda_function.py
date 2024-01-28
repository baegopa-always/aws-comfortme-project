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

def  conductSqlQuery(sql,email):
    print("--------------------------------")
    print("conductSqlQuery function init")
    conn=getMysqlConn()
    curs = conn.cursor()
    with conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql,email)
                # result = json.dumps(cur.fetchall(),default=json_default,ensure_ascii = False)
                result = cur.fetchall()
    print("conductSqlQuery function done")
    print("--------------------------------")
    return result


def handler(event, context):
    try:
        print("--------------------------------")
        print("recommendUserConsolePost lambda_handler function init")
        params=event['queryStringParameters']
        email=params['email']
        print("email : ",email)
        
        sql = "SELECT * FROM UserEmbedding WHERE email=%s"
        user=conductSqlQuery(sql,email)
        if len(user)==0:
            return  {
            'statusCode':200,
            'body': "아직 고민글을 한번도 작성하지 않으셨어요! 추천해드릴만한 고민글이 없네요",
            'headers': {
                'Access-Control-Allow-Origin': '*'}}
        user=user[0]
        
        userBertEmbedding=np.fromstring(user['bertEmbedding'].replace('[','').replace(']',''),sep=', ')
        print("userBertEmbedding:", userBertEmbedding)
        
        sql = "SELECT * FROM ConsolePost WHERE email!=%s AND bertEmbedding IS NOT NULL "
        consolePosts=conductSqlQuery(sql,email)

        df=pd.DataFrame(consolePosts)
        df['bertEmbedding']=df['bertEmbedding'].apply(lambda x:np.fromstring(x.replace('[','').replace(']',''),sep=', '))
        print("df :", type(df))

        df['similarity'] = df['bertEmbedding'].map(lambda x: cosine_similarity([userBertEmbedding], [x]).squeeze())
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

