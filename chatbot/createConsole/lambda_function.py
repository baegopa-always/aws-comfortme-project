import json
import sys
import logging
import pymysql
import boto3
from http import HTTPStatus
import requests

def getMysqlConn():
    return pymysql.connect(
            host=DB_HOST, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            db=DB_NAME)

def  conductSqlQuery(sql, sqlData):
    print("--------------------------------")
    print("conductSqlQuery function init")
    conn=getMysqlConn()
    curs = conn.cursor()
    curs.execute(sql, sqlData)
    consolePostId=curs.lastrowid
    conn.commit()
    print("conductSqlQuery function done")
    print("--------------------------------")
    return consolePostId
    
def lambda_handler(event, context):
    try:
        print("--------------------------------")
        print("createConsolePost lambda_handler function init")
        print("event : ",event)
        
        data=json.loads(event['body'])
        
        title=data['title']
        contents=data['contents']
        email=data['email']
        anonymous=data['anonymous']
        mainCategory=data['mainCategory']
        subCategory=data['subCategory']
        print(f"title : {title}   contents : {contents}   anonymous : {anonymous}   mainCategory : {mainCategory}   subCategory : {subCategory}")
        
        
        
        
        comprehend = boto3.client(service_name='comprehend', region_name='ap-northeast-2',aws_access_key_id='AKIAUI2WSCLQZYBOH6L7', aws_secret_access_key='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')
        retVal=comprehend.detect_sentiment(Text=contents, LanguageCode='ko')
        
        
        
        sentimentScore=retVal['SentimentScore']
        positive=sentimentScore['Positive']
        negative=sentimentScore['Negative']
        
        
        sql = "INSERT INTO ConsolePost(title,contents,email,anonymous,mainCategory,subCategory,positive,negative) VALUES(%(title)s,%(contents)s,%(email)s,%(anonymous)s,%(mainCategory)s,%(subCategory)s,%(positive)s,%(negative)s)"
        sqlData={
            'title':title,
            'contents':contents,
            'email':email,
            'anonymous':anonymous,
            'mainCategory':mainCategory,
            'subCategory':subCategory,
            'positive':positive,
            'negative':negative
        }
        consolePostId=conductSqlQuery(sql,sqlData)
        print("consolePostId : ",consolePostId )
        
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        requests.post('https://x3zh92gyl0.execute-api.ap-northeast-2.amazonaws.com/default/console-post', headers=headers,timeout=100,json={'contents':contents,'consolePostId':consolePostId})
        
        result={'statusCode':HTTPStatus.OK,'headers': {
                'Access-Control-Allow-Origin': '*',
            }
        }
        print("createConsolePost lambda_handler function done")
        print("--------------------------------")
        return result
    except Exception:
        logging.exception(Exception)
