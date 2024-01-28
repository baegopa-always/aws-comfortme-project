import json
import logging
import pymysql
import datetime
from http import HTTPStatus
import sys
import requests

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
        result = json.dumps(cursor.fetchall())
    return result

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d %H:%M:%S') 
    raise TypeError('not JSON serializable')

def lambda_handler(event, context):
    try:
        params=event['queryStringParameters']
        consolePostId=params['consolePostId']
        print("consolePostId : ",consolePostId)
        sqlData={
            'consolePostId':consolePostId
        }
        sql = "SELECT COUNT(*) AS 'cheerUpCount' FROM CheerUp WHERE consolePostId=%(consolePostId)s"
        value=getCheerUpSQL(sql,sqlData)
        
        result={
            'statusCode':HTTPStatus.OK,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body':value
        }
        return result
    except Exception:
        logging.exception(Exception)