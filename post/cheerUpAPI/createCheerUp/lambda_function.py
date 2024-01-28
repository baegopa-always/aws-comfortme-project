import json
import logging
import pymysql
import sys
import requests
from http import HTTPStatus
import datetime

DB_HOST="db-team8-consolation.c8fut6pj2ay8.ap-northeast-2.rds.amazonaws.com"
DB_USER="root"
DB_PASSWORD="1tkddydwkdql"
DB_NAME="comfortmeDB"

def connectSQL():
    return pymysql.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        db=DB_NAME)
    
def getCheerUpSQL(sql,sqlData):
    connection=connectSQL()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql,sqlData)
        result = json.dumps(cursor.fetchall(),default=json_default,ensure_ascii = False)
    return result


def createCheerUpSQL(sql,sqlData):
    connection=connectSQL()
    connection.cursor().execute(sql, sqlData) 
    connection.commit()

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d %H:%M:%S') 
    raise TypeError('not JSON serializable')


def lambda_handler(event, context):
    try:
        data=json.loads(event['body'])
        
        consolePostId=data['consolePostId']
        email=data['email']
        print(f"consolePostId : {consolePostId}   email : {email}")

        sqlData={
            'consolePostId':consolePostId,
            'email':email
        }
        sql = "SELECT * FROM CheerUp WHERE consolePostId= %(consolePostId)s AND email=%(email)s"
        value=getCheerUpSQL(sql,sqlData)
        print("value : ", value)
        if str(value)!="[]":
            result={'statusCode':HTTPStatus.BAD_REQUEST, 'body':"이미 힘내요를 누르셨습니다."}
            return result
        
        sql = "INSERT INTO CheerUp(consolePostId,email) VALUES(%(consolePostId)s,%(email)s)"
        createCheerUpSQL(sql,sqlData)
        
        result={
            'statusCode':HTTPStatus.OK,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            }
        }
        return result
    except Exception:
        logging.exception(Exception)
