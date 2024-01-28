import json
import sys
import logging
import pymysql
import datetime
from http import HTTPStatus

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

def getCategoryPosts(sql,sqlData):
    connection=connectSQL()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql,sqlData)
        result = json.dumps(cursor.fetchall(),default=json_default,ensure_ascii = False)
    return result

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d %H:%M:%S') 
    raise TypeError('not JSON serializable')

def lambda_handler(event, context):
    try:
        print("event : ",event)
        params=event['queryStringParameters']

        category=params['mainCategory']
        page=params['page']
        print("mainCategory : ",category, "page : ",page)
        
        mainCategory,subCategory=category.split("/")
        mainCategory=f"%{mainCategory}%"
        subCategory=f"%{subCategory}%"
        
        limit=str(10)
        offset=str(int(page)*10)
        
        sql = f"select cp.*, (select count(*) from Comment c where c.consolePostId=cp.consolePostId) as commentCount,(select count(*) from CheerUp ch where ch.consolePostId=cp.consolePostId) as cheerUpCount from ConsolePost cp WHERE (cp.mainCategory LIKE {mainCategory} OR cp.subCategory LIKE {subCategory}) ORDER BY cp.createdAt DESC LIMIT {limit} OFFSET {offset}"
        sqlData={
            'mainCategory':mainCategory,
            'subCategory':subCategory
        }
        value=getCategoryPosts(sql,sqlData)
        
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